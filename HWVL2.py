def o(text):
  ORD = []
  for i in text:
    ORD.append(ord(i))
  return ORD

def HWVL(text="" , output_len=32):
  if text=="" or output_len==0:return ""
  for i in range(50):
    my_ord = o(text)
    output = ""
    for i in range(len(my_ord)-1):
      output+=chr(33+((my_ord[i]*my_ord[i+1])%94))
    output+=chr(my_ord[-1])

  while len(output) % output_len  != 0 :
    if output_len < len(text) :
      output = output[:-1]
    elif len(output) % output_len != 0 :
      output="!"+output
    for i in range(50):
      my_ord = o(output)
      output = ""
      for i in range(len(my_ord)-1):
        output+=chr(33+((my_ord[i]*my_ord[i+1])%94))
      output+=chr(33+((my_ord[0]*my_ord[1]//my_ord[-1])%94))
 
  return "".join(chr(33+(sum(ord(output[i*output_len:(i+1)*output_len][j]) for i in range(len(output)//output_len))%94)) for j in range(output_len))