def subset w
    d=1+rand w.max
    a=w.map {|i| i%d}.reject {|i| i.zero?}
    possibilities=subset(a)
    test possibilities
end