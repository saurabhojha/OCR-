'''
    This is the eight process in ocr!!

        Use before this: pre_recognition processing

        Use after this:  output_file_opener


'''
def text_generation(list1,output_list):
    ref_list = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    output = []
    c = 0
    for k in range(len(list1)):
      t1 = list1[k]
      for j in range(len(t1)):
        t2 = t1[j]
        t = []
        for i in range(len(t2)):
          t.append(ref_list[output_list[c]])
          c = c + 1
        t = "".join(t)
        t=t.lower()
        output.append(t)
        output.append(" ")
      output.append("\n")
    output = "".join(output)
    fileName = "recognised_text.txt"
    f = open("recognised_text.txt","w+")
    f.write(output)
    f.close()
    print('Recognition done!! Opening file:')
    return fileName
