import execjs

if __name__ == '__main__':
    func = "function filter(deviceSAAndEP, key, value){if (deviceSAAndEP=='098001' && key == 'alarm' && value==1){return true;}else{return false;}}"
           
    deviceSAAndEP = "098001"
    key = 'alarm'
    value = 1.0
    
    print(func)
    ctx = execjs.compile(func)
    
    a = ctx.call("filter", deviceSAAndEP, key, value)
    print(a)
    # print(int('0005'))