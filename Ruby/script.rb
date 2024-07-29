$x=1
$a=[5, 10, 8, 15]
$w=13
$c={}
$b=[1]
$a.each do |i|
    $c[$x]=i
    if(i<=w)
        ($x|=$x<<i)%(1<<w)
    $b<<$x
end

#$b.reverse.each {|i| printf "%b\n", i}

def printsum(w,b)
    prev=nil
    curr=nil
    #puts "\nb is"
    #b.each {|i| printf "%b\n", i}
    #puts
    b.each_with_index do |obj, i|
        prev=curr
        curr=obj[w]==1
        #printf "prev: %s; curr: %s\n", prev, curr
        if(prev && !curr)
            puts $c[obj]
            printsum(w-$c[obj], b[i..-1])
            break
        end
    end
end

printsum($w,$b.reverse)