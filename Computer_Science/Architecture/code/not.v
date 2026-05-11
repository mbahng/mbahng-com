module not(
  input x, 
  output y
); 
  nand nand1(y, x, x);
endmodule
