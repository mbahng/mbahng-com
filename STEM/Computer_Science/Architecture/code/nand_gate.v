module nand_gate(
  input a, b,
  output y
);
  assign y = ~(a & b);
endmodule

module nand_gate_tb;
  reg a, b; // registers that hold states
  wire y;

  // Instantiate device under test
  nand_gate dut(.a(a), .b(b), .y(y));

  initial begin
    // Enable waveform dumping
    $dumpfile("nand_gate.vcd");
    $dumpvars(0, nand_gate_tb);

    // Test all input combinations
    a = 0; b = 0; #10;
    a = 0; b = 1; #10;
    a = 1; b = 0; #10;
    a = 1; b = 1; #10;

    $display("Test complete");
    $finish;
  end

  // Monitor changes
  initial
    $monitor("At time %t: a=%b, b=%b, y=%b", $time, a, b, y);
endmodule
