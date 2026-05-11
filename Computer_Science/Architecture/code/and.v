module and(
  input x1, x2
  output y
);
  wire z1;

  nand nand1(z1, x1, x2);
  nand nand2(y, z1, z1);
endmodule
