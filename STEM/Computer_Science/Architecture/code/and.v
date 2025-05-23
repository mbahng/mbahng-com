module multiplex_gate_level(A, B, X, out1);
  input A, B, X;
  output out1;

  wire not_x;
  wire out_and1, out_and2;

  not not1(not_X, X);
  and and1(out_and1, not_X, A);
  and and2(out_and2, X, B);
  or or1(out1, out_and1, out_and2);
endmodule

module tb_multiplex;
  reg A, B, X;
  wire out1;

  multiplex_gate_level uut(A, B, X, out1);

  initial begin
    // Test all combinations
    A = 0; B = 0; X = 0; #10;
    A = 0; B = 1; X = 0; #10;
    A = 1; B = 0; X = 0; #10;
    A = 1; B = 1; X = 0; #10;
    A = 0; B = 0; X = 1; #10;
    A = 0; B = 1; X = 1; #10;
    A = 1; B = 0; X = 1; #10;
    A = 1; B = 1; X = 1; #10;
    $finish;
  end

  initial begin
    $dumpfile("waves.vcd");
    $dumpvars(0, tb_multiplex);
  end
endmodule
