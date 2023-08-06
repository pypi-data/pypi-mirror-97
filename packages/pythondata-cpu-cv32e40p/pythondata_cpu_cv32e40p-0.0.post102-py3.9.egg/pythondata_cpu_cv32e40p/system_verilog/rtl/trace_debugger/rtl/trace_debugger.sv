// Copyright 2018 Robert Balas
// Copyright and related rights are licensed under the Solderpad Hardware
// License, Version 0.51 (the "License"); you may not use this file except in
// compliance with the License.  You may obtain a copy of the License at
// http://solderpad.org/licenses/SHL-0.51. Unless required by applicable law
// or agreed to in writing, software, hardware and materials distributed under
// this License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
// CONDITIONS OF ANY KIND, either express or implied. See the License for the
// specific language governing permissions and limitations under the License.
//
// Author: Robert Balas (balasr@student.ethz.ch)
// Description: Compress instruction traces and filter them

`define SYNTHESIS

import trdb_pkg::*;

module trace_debugger
    #(parameter APB_ADDR_WIDTH = 32)
    (input logic                clk_i,
     input logic                rst_ni,
     input logic                test_mode_i,

     // data from the cpu
     input logic                ivalid_i, //TODO: pipelined valid
     input logic                iexception_i,
     input logic                interrupt_i,
     input logic [CAUSELEN-1:0] cause_i,
     input logic [XLEN-1:0]     tval_i,
     input logic [PRIVLEN-1:0]  priv_i,
     input logic [XLEN-1:0]     iaddr_i,
     input logic [ILEN-1:0]     instr_i,
     input logic                compressed_i,

     // APB interface
     input logic [31:0]         paddr_i,
     input logic [31:0]         pwdata_i,
     input logic                pwrite_i,
     input logic                psel_i,
     input logic                penable_i,
     output logic [31:0]        prdata_o,
     output logic               pready_o,
     output logic               pslverr_o,

     // generated packets, which go the the udma (or somewhere else)
     output logic [XLEN-1:0]    packet_word_o,
     output logic               packet_word_valid_o,
     input logic                grant_i);


    // general control of this module
    // clock enabled
    logic                       trace_enable;
    logic                       clk_gated;
    // tracing enabled
    logic                       trace_activated;
    // proper privileges for debugging
    logic                       debug_mode;
    // whether input is good
    logic                       trace_valid;
    // control the streamer unit
    logic                       flush_stream;
    logic                       flush_confirm;
    // control the packet fifo
    logic                       clear_fifo;
    logic                       fifo_overflow;
    // special case to jump over vector table entries (which can't be inferred
    // by inspecting the programs' executable
    logic                       packet_after_exception;

    logic                       trace_full_addr;

    // register all inputs, we don't want to extend riscy's paths
    logic                       ivalid_q, ivalid_d;
    logic                       iexception_q, iexception_d;
    logic                       interrupt_q, interrupt_d;
    logic [CAUSELEN-1:0]        cause_q, cause_d;
    // logic [XLEN-1:0]            tval_d, tval_q;
    logic [PRIVLEN-1:0]         priv_q, priv_d;
    logic [XLEN-1:0]            iaddr_q, iaddr_d;
    logic [ILEN-1:0]            instr_q, instr_d;
    logic                       compressed_q, compressed_d;


    // unused variables for a more extensive implementation
    // riscy doesn't have those features
    logic [XLEN-1:0]            lc_tval;
    logic [CONTEXTLEN-1:0]      tc_context;


    // we have three phases, called next cycle (nc), this cycle (tc) and next
    // cycle (nc), based on which we make decision whether we need to emit a
    // packet or not.
    logic [PRIVLEN-1:0]         nc_priv, tc_priv;
    logic                       nc_privchange, tc_privchange;
    logic                       nc_exception, lc_exception;
    logic                       lc_u_discontinuity;
    logic                       tc_first_qualified;
    logic                       tc_is_branch;
    logic                       tc_branch_taken;
    logic                       tc_qualified, lc_qualified, nc_qualified,
                                nc_unqualified;
    logic                       tc_compressed;
    logic [XLEN-1:0]            tc_iaddr, nc_iaddr;
    logic                       lc_exception_sync;
    logic                       lc_interrupt;

    // pass delayed data
    logic [CAUSELEN-1:0]        lc_cause;

    // registers to hold onto the input data for a few phases, mostly one
    logic                       interrupt0_q, interrupt0_d;
    logic                       interrupt1_q, interrupt1_d;
    logic [CAUSELEN-1:0]        cause0_q, cause0_d;
    logic [CAUSELEN-1:0]        cause1_q, cause1_d;
    logic [PRIVLEN-1:0]         priv0_q, priv0_d;
    logic                       privchange0_q, privchange0_d;
    logic                       exception0_q, exception0_d,
                                exception1_q, exception1_d,
                                exception2_q, exception2_d;
    logic                       u_discontinuity0_q, u_discontinuity0_d,
                                u_discontinuity1_q, u_discontinuity1_d;
    logic                       is_branch0_q, is_branch0_d;
    logic                       compressed0_q, compressed0_d;
    logic [XLEN-1:0]            iaddr0_q, iaddr0_d;
    logic                       qualified0_q, qualified0_d, qualified1_q,
                                qualified1_d;

    // variables for discontinuity decision making
    logic                       trace_implicit_ret;
    logic                       not_ret;
    logic                       really_c_jalr;
    logic                       really_c_jr;
    logic                       is_ret;
    logic                       is_c_ret;
    logic                       is_jump;
    logic                       is_priv_ret;

    // variables for the branch map
    logic                       branch_map_flush;
    logic                       branch_map_full;
    logic                       branch_map_empty;
    logic [30:0]                branch_map;
    logic [4:0]                 branch_map_cnt;

    // variables for the packet generation
    logic                       packet_valid;
    trdb_format_e               packet_format;
    trdb_subformat_e            packet_subformat;

    // variables for address compression
    logic [$clog2(XLEN)-1+1:0]  keep_addr_bits;
    logic [XLEN-1:0]            diff_addr;

    // generated packet
    logic [PACKET_LEN-1:0]     packet_gen_bits;
    logic [6:0]                packet_gen_len;
    logic                      packet_gen_valid;

    // packet from fifo
    logic [PACKET_LEN-1:0]     packet_fifo_bits;
    logic [6:0]                packet_fifo_len;
    logic                      packet_fifo_valid;
    logic                      packet_fifo_not_full;

    // packet to word
    logic                      packet_is_read;
    logic [XLEN-1:0]           packet_word;
    logic                      packet_word_valid;

    // Holds data from/to advanced peripheral bus
    logic [31:0]               per_rdata;
    logic                      per_ready;
    logic [31:0]               per_wdata;
    logic [APB_ADDR_WIDTH-1:0] per_addr;
    logic                      per_we;
    logic                      per_valid;

    // software dumping: certain writes to the trace debugger are included in
    // the packet stream
    logic [31:0]               sw_word;
    logic                      sw_valid;
    logic                      sw_grant;

    // timer unit
    logic                      timer_rst;
    logic [TIMER_WIDTH-1:0]    tu_time;
    logic                      tu_fulltime;
    logic                      tu_grant;
    logic                      tu_valid;
    logic                      tu_req;

    // filter unit
    logic                      apply_filters;
    logic                      trace_selected_priv;
    logic [1:0]                trace_which_priv;
    logic                      trace_range_event;
    logic                      trace_stop_event;
    logic [XLEN-1:0]           trace_lower_addr;
    logic [XLEN-1:0]           trace_higher_addr;
    logic                      filter_qualified_decision;
    logic                      trace_req_deactivate;
    logic                      trace_range_match;
    logic                      trace_priv_match;

    // TODO: send this to reg
    assign timer_rst = '0;

    // to register all inputs
    assign ivalid_d = ivalid_i;
    assign iexception_d = iexception_i;
    assign interrupt_d = interrupt_i;
    assign cause_d  = cause_i;
    assign priv_d = priv_i;
    assign iaddr_d = iaddr_i;
    assign instr_d = instr_i;
    assign compressed_d = compressed_i;

    // whether we do tracing at all
    assign trace_valid = ivalid_q && debug_mode && trace_enable;
    assign debug_mode = priv_q[PRIVLEN-1];

    // TODO: make this configurationr register mapped
    assign packet_after_exception                      = '1;

    // unimplemented, just tie to zero
    assign lc_tval = '0;
    assign tc_context = '0;

`ifndef SYNTHESIS
    trace_valid_and_debug: assert property
    (@(posedge clk_gated) disable iff (~rst_ni) (trace_enable |=> debug_mode))
        else $info("[TRDB]    @%t: Tracing works only in debug mode",
                   $time);
`endif

    // Buffer variables. Certain variables we need to hold up to three cycles
    assign interrupt0_d = interrupt_q;
    assign interrupt1_d = interrupt0_q;
    assign cause0_d = cause_q;
    assign cause1_d = cause0_q;
    assign priv0_d = priv_q;
    assign exception0_d = iexception_q && ivalid_q;
    assign exception1_d = exception0_q;
    assign exception2_d = exception1_q;
    assign compressed0_d = compressed_q;
    assign iaddr0_d = iaddr_q;

    // assign privchange0_d (below)
    // assign u_discontinuity0_d (below)
    // assign is_branch0_d (below)

    assign u_discontinuity1_d = u_discontinuity0_q;
    // TODO: add feature to have selective tracing, add enable with regmap
    assign qualified0_d = trace_enable && filter_qualified_decision; //& ivalid_q
    assign qualified1_d = qualified0_q;

    // Hook phase related variables up to proper register
    assign nc_priv = priv0_d;
    assign tc_priv = priv0_q;
    assign lc_interrupt = interrupt1_q;
    assign lc_cause = cause1_q;
    assign nc_privchange = privchange0_d;
    assign tc_privchange = privchange0_q;
    assign nc_exception = exception0_d;
    assign lc_exception = exception1_q;
    // with that variable we force another packet after an exception packet, so
    // that we don't need to know the vector table entries
    assign lc_exception_sync = exception2_q;
    assign lc_u_discontinuity = u_discontinuity1_q;
    assign tc_is_branch = is_branch0_q;
    assign nc_qualified = qualified0_d;
    assign tc_qualified = qualified0_q;
    assign lc_qualified = qualified1_q;
    assign tc_compressed = compressed0_q;
    assign nc_iaddr = iaddr0_d;
    assign tc_iaddr = iaddr0_q;
    // assign tc_first_qualified (below)
    // assign tc_branch_taken (below)

    // determine if we are allowed to emit packets for nc (next cycle)
    trdb_filter i_trdb_filter
        (.trace_activated_i(trace_activated),
         .trace_req_deactivate_o(trace_req_deactivate),
         .apply_filters_i(apply_filters),
         .trace_selected_priv_i(trace_selected_priv),
         .which_priv_i(trace_which_priv),
         .priv_i(priv_d[1:0]),
         .trace_range_event_i(trace_range_event),
         .trace_stop_event_i(trace_stop_event),
         .trace_lower_addr_i(trace_lower_addr),
         .trace_higher_addr_i(trace_higher_addr),
         .iaddr_i(iaddr_d),
         .trace_range_match_o(trace_range_match),
         .trace_priv_match_o(trace_priv_match),
         .trace_qualified_o(filter_qualified_decision));


    // decide whether a privilege change occured
    always_comb begin
        privchange0_d = (tc_priv != nc_priv) && ivalid_q;
    end

    // decide whether we have a branch instruction
    // beq, bne, blt, bge, bltu, bgeu, p_bneimm, p_beqimm
    always_comb begin: is_branch
        is_branch0_d
            = ((instr_q & MASK_BEQ)      == MATCH_BEQ) ||
              ((instr_q & MASK_BNE)      == MATCH_BNE) ||
              ((instr_q & MASK_BLT)      == MATCH_BLT) ||
              ((instr_q & MASK_BGE)      == MATCH_BGE) ||
              ((instr_q & MASK_BLTU)     == MATCH_BLTU) ||
              ((instr_q & MASK_BGEU)     == MATCH_BGEU) ||
              ((instr_q & MASK_P_BNEIMM) == MATCH_P_BNEIMM) ||
              ((instr_q & MASK_P_BEQIMM) == MATCH_P_BEQIMM) ||
              ((instr_q & MASK_C_BEQZ)   == MATCH_C_BEQZ) ||
              ((instr_q & MASK_C_BNEZ)   == MATCH_C_BNEZ);
    end

    // decide whether we have a unpredictable discontinuity
    // jalr, mret, sret, uret
    always_comb begin: is_discontinuity

        really_c_jalr = ((instr_q & MASK_C_JALR) == MATCH_C_JALR)
                        && ((instr_q & MASK_RD) != 0);

        really_c_jr = ((instr_q & MASK_C_JR) == MATCH_C_JR)
                      && ((instr_q & MASK_RD) != 0);

        is_jump = ((instr_q & MASK_JALR) == MATCH_JALR) ||
                  really_c_jalr || really_c_jr;

        is_priv_ret = ((instr_q & MASK_MRET) == MATCH_MRET) ||
                  ((instr_q & MASK_SRET) == MATCH_SRET) ||
                  ((instr_q & MASK_URET) == MATCH_URET);

        // allows us to mark ret's as not being discontinuities, if we want
        not_ret = '1;
        is_ret = ((instr_q & (MASK_JALR | MASK_RD | MASK_RS1 | MASK_IMM)) ==
                 (MATCH_JALR | (X_RA << OP_SH_RS1)));
        is_c_ret = (instr_q & (MASK_C_JR | MASK_RD)) ==
                   (MATCH_C_JR | (X_RA << OP_SH_RD));

        if(trace_implicit_ret)
            not_ret = !(is_ret || is_c_ret);

        u_discontinuity0_d = (is_jump || is_priv_ret) && not_ret;
    end

    // figure out whether we are dealing with the first qualified instruction
    always_comb begin: is_qualified
        tc_first_qualified = !lc_qualified && tc_qualified;
    end

    always_comb begin: becomes_unqualified
        nc_unqualified = !nc_qualified;
    end

    // is this branch taken?
    // TODO: change to tc_compressed? 2 :4
    always_comb begin: is_branch_taken
        tc_branch_taken = tc_compressed ?
                          !(tc_iaddr + 2 == nc_iaddr):
                          !(tc_iaddr + 4 == nc_iaddr);
    end

    // update branch map, careful there is a direct combinatorial path
    trdb_branch_map i_trdb_branch_map
        (.clk_i(clk_gated),
         .rst_ni(rst_ni),
         .valid_i(tc_is_branch && trace_valid && tc_qualified),
         .branch_taken_i(tc_branch_taken),
         .flush_i(branch_map_flush),
         .map_o(branch_map),
         .branches_o(branch_map_cnt),
         .is_full_o(branch_map_full),
         .is_empty_o(branch_map_empty));

    // decides, by looking at the history of instructions, whether a packet is
    // necessary or not
    trdb_priority i_trdb_priority
        (// there might be some data stuck in the
         // pipeline if valid never goes high again (e.g.
         // after wfi), but this shouldnt matter
         .valid_i(trace_valid && tc_qualified),
         .full_addr_i(tc_iaddr),
         .diff_addr_i(diff_addr),
         .lc_exception_i(lc_exception),
         .lc_exception_sync_i(lc_exception_sync && packet_after_exception),

         .tc_first_qualified_i(tc_first_qualified),
         .nc_unqualified_i(nc_unqualified),

         //input logic  tc_unhalted,
         .tc_privchange_i(tc_privchange),
         //input logic resync & branch_map_cnt

         .lc_u_discontinuity_i(lc_u_discontinuity),

         // input logic  resync
         // input logic  branch_map_nonempty,

         //input logic  nc_halt,
         .nc_exception_i(nc_exception),
         .nc_privchange_i(nc_privchange),
         //input logic  nc_qualified,

         .branch_map_full_i(branch_map_full),

         //input logic  tc_context_change,
         .branch_map_empty_i(branch_map_empty),
         .use_full_addr_i(trace_full_addr),
         .keep_bits_o(keep_addr_bits),
         .valid_o(packet_valid),
         .packet_format_o(packet_format),
         .packet_subformat_o(packet_subformat));


    // keep track of time for time packets
    trdb_timer
        #(.TIMER_WIDTH(TIMER_WIDTH))
    i_trdb_timer
        (.clk_i(clk_gated),
         .rst_ni(rst_ni),
         .manual_rst_i(timer_rst),
         .tu_req_i(tu_req),
         .tu_valid_o(tu_valid),
         .tu_grant_i(tu_grant),
         .trdb_time_o(tu_time));


    // whole packet generation logic
    trdb_packet_emitter i_trdb_packet_emitter
        (.clk_i(clk_gated),
         .rst_ni(rst_ni),
         .packet_format_i(packet_format),
         .packet_subformat_i(packet_subformat),
         .keep_bits_i(keep_addr_bits),
         .valid_i(packet_valid),
         .use_full_addr_i(trace_full_addr),
         .interrupt_i(lc_interrupt), // get the value of the trapped instr
         .cause_i(lc_cause),
         .tval_i(lc_tval),
         .priv_i(tc_priv),
         .iaddr_i(tc_iaddr),
         .context_i(tc_context),
         .lc_u_discontinuity_i(lc_u_discontinuity),
         .branch_map_i(branch_map),
         .branch_map_cnt_i(branch_map_cnt),
         .branch_map_empty_i(branch_map_empty),
         .branch_map_full_i(branch_map_full),
         .is_branch_i(tc_is_branch),
         .branch_map_flush_o(branch_map_flush),
         .diff_addr_o(diff_addr),
         .sw_valid_i(sw_valid),
         .sw_word_i(sw_word),
         .sw_grant_o(sw_grant),
         .tu_valid_i(tu_valid),
         .tu_time_i(tu_time),
         .tu_fulltime_i(tu_fulltime),
         .tu_grant_o(tu_grant),
         .packet_bits_o(packet_gen_bits),
         .packet_len_o(packet_gen_len),
         .packet_valid_o(packet_gen_valid));

    //TODO: implement fifo clear logic
    //TODO: request resync logic on nuked fifo
    assign clear_fifo = 1'b0;
    assign fifo_overflow = ~packet_fifo_not_full;

    // this buffers our generated packet, since packets can be generated every
    // cycle, but we only read atmost 32 bit per cycle
    generic_fifo_adv
        #(.DATA_WIDTH(PACKET_LEN + $clog2(PACKET_LEN)),
          .DATA_DEPTH(PACKET_BUFFER_STAGES))
    i_packet_fifo
        (.clk(clk_i),
         .rst_n(rst_ni),
         .clear_i(clear_fifo), //clear fifo if overflowing
         .data_i({packet_gen_bits, packet_gen_len}),
         .valid_i(packet_gen_valid),
         .grant_o(packet_fifo_not_full),
         .data_o({packet_fifo_bits, packet_fifo_len}),
         .valid_o(packet_fifo_valid),
         .grant_i(packet_is_read),
         .test_mode_i('0)); // TODO: what to do with this

`ifndef SYNTHESIS
    packet_fifo_overflow: assert property
    (@(posedge clk_i) disable iff (~rst_ni) (packet_fifo_not_full == 1'b1))
            else $error("[TRDB]   @%t: Packet FIFO is overflowing.", $time);
`endif

    trdb_align8 i_trdb_align8
        (.clk_i(clk_gated),
         .rst_ni(rst_ni),
         .payload_bits_i(packet_fifo_bits),
         .payload_len_i(packet_fifo_len),
         .valid_i(packet_fifo_valid),
         .grant_o(packet_is_read),
         .flush_stream_i(flush_stream),
         .flush_confirm_o(flush_confirm),
         .data_o(packet_word),
         .grant_i(grant_i),
         .valid_o(packet_word_valid));

    assign packet_word_o = packet_word;
    assign packet_word_valid_o = packet_word_valid;

    // TODO: assert that we are not dealing with an unsupported instruction
    always_ff @(posedge clk_gated, negedge rst_ni) begin
        if(~rst_ni) begin
            ivalid_q           <= '0;
            iexception_q       <= '0;
            interrupt_q        <= '0;
            cause_q            <= '0;
            priv_q             <= '0;
            iaddr_q            <= '0;
            instr_q            <= '0;
            compressed_q       <= '0;

            interrupt0_q       <= '0;
            interrupt1_q       <= '0;
            cause0_q           <= '0;
            cause1_q           <= '0;
            priv0_q            <= 3'h7; //we always start in M-mode
            privchange0_q      <= '0;
            exception0_q       <= '0;
            exception1_q       <= '0;
            exception2_q       <= '0;
            u_discontinuity0_q <= '0;
            u_discontinuity1_q <= '0;
            is_branch0_q       <= '0;
            compressed0_q      <= '0;
            iaddr0_q           <= '0;
            qualified0_q       <= '0;
            qualified1_q       <= '0;
        end else begin
            ivalid_q     <= ivalid_d;
            iexception_q <= iexception_d;
            interrupt_q  <= interrupt_d;
            cause_q      <= cause_d;
            priv_q       <= priv_d;
            iaddr_q      <= iaddr_d;
            instr_q      <= instr_d;
            compressed_q <= compressed_d;

            if(ivalid_q) begin
                interrupt0_q       <= interrupt0_d;
                interrupt1_q       <= interrupt1_d;
                cause0_q           <= cause0_d;
                cause1_q           <= cause1_d;
                priv0_q            <= priv0_d;
                privchange0_q      <= privchange0_d;
                exception0_q       <= exception0_d;
                exception1_q       <= exception1_d;
                exception2_q       <= exception2_d;
                u_discontinuity0_q <= u_discontinuity0_d;
                u_discontinuity1_q <= u_discontinuity1_d;
                is_branch0_q       <= is_branch0_d;
                compressed0_q      <= compressed0_d;
                iaddr0_q           <= iaddr0_d;
                qualified0_q       <= qualified0_d;
                qualified1_q       <= qualified1_d;
            end
        end
    end

    // Connection to the APB. Used to configure the trace debugger. This is just
    // a translation layer.
    trdb_apb_if
        #(.APB_ADDR_WIDTH(APB_ADDR_WIDTH))
    i_trdb_apb_if
        (.paddr(paddr_i),
         .pwdata(pwdata_i),
         .pwrite(pwrite_i),
         .psel(psel_i),
         .penable(penable_i),
         .prdata(prdata_o),
         .pready(pready_o),
         .pslverr(pslverr_o),

         .per_rdata_i(per_rdata),
         .per_ready_i(per_ready),
         .per_wdata_o(per_wdata),
         .per_addr_o(per_addr),
         .per_we_o(per_we),
         .per_valid_o(per_valid));

    // Holds configuration data written from the APB and asserts relevant
    // control signals depending on that
    trdb_reg
        #(.APB_ADDR_WIDTH(APB_ADDR_WIDTH))
    i_trdb_reg
        (.clk_i(clk_i),
         .rst_ni(rst_ni),
         .test_mode_i(test_mode_i),
         .clk_gated_o(clk_gated),
         .per_rdata_o(per_rdata),
         .per_ready_o(per_ready),
         .per_wdata_i(per_wdata),
         .per_addr_i(per_addr),
         .per_we_i(per_we),
         .per_valid_i(per_valid),
         .flush_stream_o(flush_stream),
         .flush_confirm_i(flush_confirm),
         .clear_fifo_o(), // TODO: connect
         .trace_enable_o(trace_enable),
         .trace_activated_o(trace_activated),
         .trace_full_addr_o(trace_full_addr),
         .trace_req_deactivate_i(trace_req_deactivate),
         .trace_implicit_ret_o(trace_implicit_ret),
         .apply_filters_o(apply_filters),
         .trace_selected_priv_o(trace_selected_priv),
         .trace_which_priv_o(trace_which_priv),
         .trace_range_event_o(trace_range_event),
         .trace_stop_event_o(trace_stop_event),
         .trace_lower_addr_o(trace_lower_addr),
         .trace_higher_addr_o(trace_higher_addr),
         .trace_qualified_i(qualified0_d),
         .trace_priv_match_i(trace_priv_match),
         .trace_range_match_i(trace_range_match),
         .trace_fifo_overflow_i(fifo_overflow),
         .external_fifo_overflow_i(~grant_i), //external stall is a fifo overflow
         .sw_word_o(sw_word),
         .sw_valid_o(sw_valid),
         .sw_grant_i(sw_grant),
         .tu_req_o(tu_req));


endmodule // trace_debugger
