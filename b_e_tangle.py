'''Program that converts the braid to tangle for the program.
Returns a dic of elementary tangles, i.e total_dic = [1:T1, 2:T2....]
where T_i are elementary objects'''
import snappy as snap

def braid_to_tangle():
    ###### EXAMPLE CODE#####
    # 1.specify the knot by giving the arrays of size 4 , 4 , 4...
    tfoil = snap.Link([[1,4,2,5],[3,6,4,1],[5,2,6,3]])
    # 2.OR by a reserved name for the knot
    L = snap.Link('K8n1')
    
    # Approach 1. STORE THE LIST OF BRAIDWORDS
    seq = tfoil.braid_word()
    # return list of braid names 
    temp_s = list(map(abs, seq))
    # specifies the `n` for n-braid
    num_braid = max(temp_s) + 1 
    bw_len = len(seq)
    total_dic = {}
    start = num_braid
    # Specify mid section
    for i in range(bw_len):
        dic = {}
        for height in range(1, (num_braid * 2) + 1):
            s1 = (start,height)
            s2 = (start + 0.5, height)
            s3 = (start + 1, height)
            if height > num_braid:
                dic.update({s1:s2, s2:s3}) 
            else:
                dic.update({s3:s2, s2:s1})
            print("Elementary Tangle T_{0}".format(start +1 ))
            total_dic.update({start+1 : dic})
        start += 1  
    #LEFT HALF: add cups
    for i in range(num_braid):
        dic = {}
        if i == 0:
            # boundary cup
            dic.update({(0,1):(0.5,2)}) # dummy pair
            dic.update({(1,1):(1, 2 * num_braid - i)}) # cb and fix
            print("Elementary Tangle T_{0}".format(i+1))
            total_dic.update({ i+1 : dic})
        else:
            dic.update({(i+1,i+1): (i+1, (2 * num_braid) - i)}) # add cup
            for j in range(1,i+1): # rest of edges pairs
                s1 = (i,j)
                s2 = (i + 0.5,j)
                s3 = (i + 1, j)
                dic.update({s3:s2, s2:s1})
                s1 = (i, 2 * num_braid - j +1 )
                s2 = (i + 0.5, 2 * num_braid - j +1 )
                s3 = (i + 1, 2 * num_braid - j + 1)
                dic.update({s1:s2, s2:s3})
                print("Elementary Tangle T_{0}".format(i+1))
                total_dic.update({ i+1 : dic})
                
    end = 2 * num_braid + bw_len # constant
    # RIGHT HALF: add cups
    for i in range(num_braid):
        dic = {}
        if i == 0:
            # boundary cap
            dic.update({(end-0.5,1):(300,1)}) #add a dummy pair
            dic.update({(end-1, 2 * num_braid - i):(end - 1,1)})
            print("Elementary Tangle T_{0}".format(end - i))
            total_dic.update({ (end - i) : dic})
        else:
            dic.update({(end-(i+1), 2 * num_braid - i):(end-(i+1),(i+1))}) # add cap
            for j in range(1, i+1): # rest of the pairs
                s1 = (end - i, j)
                s2 = (end - i - 0.5, j)
                s3 = (end - i - 1, j)
                dic.update({s1:s2, s2:s3})
                s1 = (end - i, 2 * num_braid - j +1)
                s2 = (end - i - 0.5, 2 * num_braid - j +1)
                s3 = (end - i - 1, 2 * num_braid - j + 1)
                dic.update({s3:s2, s2:s1})    
                print("Elementary Tangle T_{0}".format(end - i))
                total_dic.update({(end - i) : dic})
                
    # take into braid word and apply swaps
    for index, braid in enumerate(seq):
        if braid > 0: # move right, i.e swap right half
            start = index + num_braid + 0.5
            dic = total_dic[start+0.5].copy()
            y_1 = abs(braid)
            y_2 = y_1 + 1
            dic.update({(start+0.5,y_2):(start,y_1),(start +0.5, y_1):(start,y_2)})
            total_dic[start+0.5] =  dic
            
        else: # movel left, i.e swap left half
            start = index + num_braid
#            print("ELSE: cur_start:{0}".format(start + 1))
            dic = total_dic[start +1].copy()
            y_1 = abs(braid)
            y_2 = y_1 + 1
            dic.update({(start+0.5,y_2):(start,y_1),(start +0.5, y_1):(start,y_2)})
#            print("ELSE: cur_start:{0}".format(start + 1))
            total_dic[start+1] = dic
#    print("+++++++")
#    for dic in total_dic.items():
#        print(dic)
#        print("\n")
#    print("final length: {0}!".format(len(total_dic)))
    return total_dic
braid_to_tangle()