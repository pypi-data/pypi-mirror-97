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
// Description: Memory mapped control registers for the trace debugger

import trdb_pkg::*;

module trdb_reg
    #(parameter APB_ADDR_WIDTH = 12)
    (input logic                      clk_i,
     input logic                      rst_ni,
     input logic                      test_mode_i,
     output logic                     clk_gated_o,

     // write and reads from the APB
     output logic [31:0]              per_rdata_o,
     output logic                     per_ready_o,
     input logic [31:0]               per_wdata_i,
     input logic [APB_ADDR_WIDTH-1:0] per_addr_i,
     input logic                      per_we_i,
     input logic                      per_valid_i,

     // packet streamer control
     output                           flush_stream_o,
     input                            flush_confirm_i,
     output logic                     clear_fifo_o,

     // trace debugger settings and control
     output logic                     trace_enable_o,
     output logic                     trace_activated_o,
     output logic                     trace_full_addr_o,
     input logic                      trace_req_deactivate_i,
     output logic                     trace_implicit_ret_o,

     // signals that control the filtering settings
     output logic                     apply_filters_o,
     output logic                     trace_selected_priv_o,
     output logic [1:0]               trace_which_priv_o,
     output logic                     trace_range_event_o,
     output logic                     trace_stop_event_o,
     output logic [XLEN-1:0]          trace_lower_addr_o,
     output logic [XLEN-1:0]          trace_higher_addr_o,

     // trace debugger status signals
     input logic                      trace_qualified_i,
     input logic                      trace_priv_match_i,
     input logic                      trace_range_match_i,
     input logic                      trace_fifo_overflow_i,
     input logic                      external_fifo_overflow_i,

     // user data writes which get merged into packet stream
     output logic [31:0]              sw_word_o,
     output logic                     sw_valid_o,
     input logic                      sw_grant_i,

     // timer packet request through user
     output logic                     tu_req_o);

    import trdb_pkg::*;

    // clock gating for everything but the ctrl register
    logic                             clk_gated;

    // hold control status
    trdb_ctrl_t ctrl_q, ctrl_d;

    // hold trace debugger status
    trdb_status_t status_q, status_d;

    // hold trace debugger filter settings
    trdb_filterconf_t filter_q, filter_d;

    // allow the user to write to this register to dump data through the trace
    // debugger
    logic [31:0] dump_q, dump_d;
    logic        dump_valid_q, dump_valid_d;
    logic        sw_fifo_not_full;
    logic        clear_sw_fifo;

    // remember address ranges
    logic [XLEN-1:0]       higher_addr_q, higher_addr_d;
    logic [XLEN-1:0]       lower_addr_q, lower_addr_d;


    // control reg outgoing signals
    assign trace_enable_o = ctrl_q.enable;
    assign trace_activated_o = ctrl_q.activated;
    assign clear_fifo_o = ctrl_q.clear_fifo;
    assign flush_stream_o = ctrl_q.flush_stream;
    assign trace_full_addr_o = ctrl_q.full_addr;
    assign trace_implicit_ret_o = ctrl_q.implicit_ret;

    // status reg outgoing signals
    assign apply_filters_o = filter_q.apply_filters;
    assign trace_selected_priv_o = filter_q.trace_priv;
    assign trace_which_priv_o = filter_q.which_priv;
    assign trace_range_event_o = filter_q.range_event[0];
    assign trace_stop_event_o = filter_q.stop_event[0];

    // for range tracing
    assign trace_lower_addr_o = lower_addr_q;
    assign trace_higher_addr_o = higher_addr_q;


    always_comb begin: read_reg
        per_rdata_o = 32'h0;
        if(per_valid_i & ~per_we_i) begin
            case(per_addr_i[7:0])
            REG_TRDB_CTRL:
                per_rdata_o = ctrl_q;
            REG_TRDB_STATUS:
                per_rdata_o = status_q;
            REG_TRDB_FILTER:
                per_rdata_o = filter_q;
            REG_TRDB_DUMP:
                per_rdata_o = 32'h0;
            REG_TRDB_DUMP_WITH_TIME:
                per_rdata_o = 32'h0;
            default:
                per_rdata_o = 32'h0;
            endcase
        end
    end


    // this buffers our software writes, since we are contesting with packets
    // which have a priority over software writes.
    generic_fifo_adv
        #(.DATA_WIDTH(32),
          .DATA_DEPTH(SOFTWARE_BUFFER_STAGES))
    i_sw_fifo
        (.clk(clk_i),
         .rst_n(rst_ni),
         .clear_i(clear_sw_fifo),
         .data_i(dump_q),
         .valid_i(dump_valid_q),
         .grant_o(sw_fifo_not_full), // TODO: make this visible in register
         .data_o(sw_word_o),
         .valid_o(sw_valid_o),
         .grant_i(sw_grant_i),
         .test_mode_i('0)); // TODO: what to do with this

`ifndef SYNTHESIS
    sw_fifo_overflow: assert property
    (@(posedge clk_i) disable iff (~rst_ni) (sw_fifo_not_full == 1'b1))
            else $error("[TRDB]   @%t: Software FIFO is overflowing.", $time);
`endif


    // we can tie this high since according the apb protocol if we react in the
    // next cycle this is allowed
    assign per_ready_o = 1'b1;


    // status from trace debugger
    assign status_d.qualified = trace_qualified_i;
    assign status_d.priv_match = trace_priv_match_i;
    assign status_d.range_match = trace_range_match_i;
    assign status_d.fifo_overflow = trace_fifo_overflow_i;
    assign status_d.ext_fifo_overflow = external_fifo_overflow_i;

    // register write logic
    always_comb begin: write_reg
        trdb_ctrl_t ctrl_w;

        ctrl_w        = '0;
        ctrl_d        = ctrl_q;
        filter_d      = filter_q;
        dump_d        = dump_q;
        dump_valid_d  = '0;
        tu_req_o      = '0;
        lower_addr_d  = lower_addr_q;
        higher_addr_d = higher_addr_q;

        if(per_valid_i & per_we_i) begin
            case (per_addr_i[7:0])
            REG_TRDB_CTRL: begin
                ctrl_w              = trdb_ctrl_t'(per_wdata_i);
                ctrl_d.activated    = ctrl_w.activated;
                ctrl_d.flush_stream = ctrl_w.flush_stream;
                ctrl_d.enable       = ctrl_w.enable;
                ctrl_d.clear_fifo   = ctrl_w.clear_fifo;
                ctrl_d.full_addr    = ctrl_w.full_addr;
                ctrl_d.implicit_ret = ctrl_w.implicit_ret;
            end
            REG_TRDB_STATUS: begin
            end
            REG_TRDB_FILTER:
                filter_d = {per_wdata_i[6], 1'b0, per_wdata_i[4:0]};
            REG_TRDB_DUMP: begin
                dump_d       = per_wdata_i;
                dump_valid_d = '1;
            end
            REG_TRDB_DUMP_WITH_TIME: begin
                dump_d       = per_wdata_i;
                dump_valid_d = '1;
                tu_req_o     = '1;
            end
            REG_TRDB_LOWER_ADDR:
                lower_addr_d = per_wdata_i;
            REG_TRDB_HIGHER_ADDR:
                higher_addr_d = per_wdata_i;
            endcase
        end

        if(flush_confirm_i)
            ctrl_d.flush_stream = 1'b0;

        // Force disable tracer when we the filter requests it. User needs to
        // change filter to allow tracing in filtered region.
        if(trace_req_deactivate_i)
            ctrl_d.activated = 1'b0;

    end

    // clock gating logic
    // pulp_clock_gating i_trdb_clock_gating
    //     (.clk_i(clk_i),
    //      .test_en_i(test_mode_i),
    //      .en_i(ctrl_q.enable),
    //      .clk_o(clk_gated));

    assign clk_gated = clk_i;

    assign clk_gated_o = clk_gated;

    always_ff @(posedge clk_i, negedge rst_ni) begin
        if(~rst_ni) begin
            ctrl_q <= 'h0;
        end else begin
            ctrl_q <= ctrl_d;
        end
    end

    always_ff @(posedge clk_gated, negedge rst_ni) begin
        if(~rst_ni) begin
            status_q      <= 'h0;
            filter_q      <= 'h0;
            dump_q        <= 'h0;
            dump_valid_q  <= 'h0;
            higher_addr_q <= 'h0;
            lower_addr_q  <= 'h0;

        end else begin
            status_q      <= status_d;
            filter_q      <= filter_d;
            dump_q        <= dump_d;
            dump_valid_q  <= dump_valid_d;
            higher_addr_q <= higher_addr_d;
            lower_addr_q  <= lower_addr_d;

        end
    end
endmodule // trdb_reg
