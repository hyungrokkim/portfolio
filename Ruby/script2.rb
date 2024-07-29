def subsetsummod a, w, k
    if a.size>=2**k then
        #use classic algorithm
    else
        k2=rand((w.div 2)-1)+1
        subsetsummod(a.map {|i| i%k2}, w%k2, k2).select {|i| verify(i,a,w,k) }
    end
end

def subsetsum a, w
    subsetsummod(a,w,(a+[w]).max)
end

def verify i, a, w, k
    b=0
    format("%0*b", a.size, i).split('').each_with_index do |obj, index|
        if obj=='1' then b+=a[index] end
    end
    w%k==b%k
end

subsetsum([5,6,10,11,15], 21).each{|i| printf "%05b\n", i}