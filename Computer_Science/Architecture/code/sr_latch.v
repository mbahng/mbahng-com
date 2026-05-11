// Gated D Latch
module gated_d_latch (
    input D, EN,
    output Q, Qn
);

wire S, R;

and (S, D, EN);
and (R, ~D, EN);
nor (Qn, R, Q);
nor (Q, S, Qn);

endmodule

// Testbench
module tb;

reg D, EN;
wire Q, Qn;

gated_d_latch dut (D, EN, Q, Qn);

initial begin
    $dumpfile("gated_d_latch.vcd");
    $dumpvars(0, tb);
    
    // Initialize
    D = 0; EN = 0; #5;
    
    // Test pattern matching the waveform
    D = 1; EN = 0; #10;  // D high, EN low
    D = 0; EN = 0; #10;  // D low, EN low
    D = 1; EN = 0; #5;   // D high, EN low
    D = 0; EN = 1; #5;   // D low, EN high
    D = 1; EN = 1; #10;  // D high, EN high
    D = 0; EN = 1; #10;  // D low, EN high
    D = 1; EN = 1; #15;  // D high, EN high
    D = 0; EN = 0; #5;   // D low, EN low
    D = 1; EN = 0; #10;  // D high, EN low
    D = 0; EN = 1; #10;  // D low, EN high
    D = 1; EN = 1; #5;   // D high, EN high
    D = 0; EN = 1; #5;   // D low, EN high
    D = 1; EN = 0; #10;  // D high, EN low
    D = 0; EN = 0; #5;   // D low, EN low
    
    $finish;
end

endmodule
