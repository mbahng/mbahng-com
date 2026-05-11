module or(
  input x1, x2, 
  output y
); 

  wire z1, z2;

  nand nand1(z1, x1, x1);
  nand nand2(z2, x2, x2); 
  nand nand3(y, z1, z2);

endmodule
