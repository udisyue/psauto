from rediscluster import StrictRedisCluster

def get_multiActi(cid, pid, hid, uid):
    nodes = [{"host": "192.168.232.14", "port": "5233"}]
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    rc00_a_c_num = r.get("acti_c%d_num"%cid)
    rc01_a_c_u_num = r.get("acti_c%d_u%d_num"%(cid, uid))
    rc10_a_c_h_num = r.get("acti_c%d_h%d_num"%(cid, hid))
    rc11_a_c_h_u_num = r.get("acti_c%d_h%d_u%d_num"%(cid, hid, uid))
    ttcost_amount = r.get("acti_c%d_amount"%cid)
    join_c_p_num = r.get("acti_c%d_p%d_num"%(cid, pid))
    jcost_a_c_p_amount = r.get("acti_c%d_p%d_amount"%(cid, pid))
    return rc00_a_c_num,rc01_a_c_u_num,rc10_a_c_h_num,rc11_a_c_h_u_num,ttcost_amount,join_c_p_num,jcost_a_c_p_amount

def get_rc00(cid):
    nodes = [{"host": "192.168.232.14", "port": "5233"}]
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    rc00_a_c_num = r.get("acti_c%d_num"%cid)
    return rc00_a_c_num

def get_rc01(cid, uid):
    nodes = [{"host": "192.168.232.14", "port": "5233"}]
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    rc01_a_c_u_num = r.get("acti_c%d_u%d_num" % (cid, uid))
    return rc01_a_c_u_num

def get_rc10(cid, hid):
    nodes = [{"host": "192.168.232.14", "port": "5233"}]
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    rc10_a_c_h_num = r.get("acti_c%d_h%d_num" % (cid, hid))
    return rc10_a_c_h_num

def get_rc11(cid, hid, uid):
    nodes = [{"host": "192.168.232.14", "port": "5233"}]
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    rc11_a_c_h_u_num = r.get("acti_c%d_h%d_u%d_num" % (cid, hid, uid))
    return rc11_a_c_h_u_num

def get_ttcost(cid):
    nodes = [{"host": "192.168.232.14", "port": "5233"}]
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    ttcost_amount = r.get("acti_c%d_amount" % cid)
    return ttcost_amount

def get_joinnum(cid, pid):
    nodes = [{"host": "192.168.232.14", "port": "5233"}]
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    join_c_p_num = r.get("acti_c%d_p%d_num" % (cid, pid))
    return join_c_p_num

def get_jcost(cid, pid):
    nodes = [{"host": "192.168.232.14", "port": "5233"}]
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    jcost_a_c_p_amount = r.get("acti_c%d_p%d_amount" % (cid, pid))
    return jcost_a_c_p_amount

def set_multiActi_value_0(cid,pid,hid,uid):
    nodes = [{"host": "192.168.232.14", "port": "5233"}]
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    rc00_a_c_num = r.set("acti_c%d_num"%cid, "0")
    rc01_a_c_u_num = r.set("acti_c%d_u%d_num"%(cid, uid),"0")
    rc10_a_c_h_num = r.set("acti_c%d_h%d_num"%(cid, hid),"0")
    rc11_a_c_h_u_num = r.set("acti_c%d_h%d_u%d_num"%(cid, hid, uid),"0")
    ttcost_amount = r.set("acti_c%d_amount"%cid,"0.0")
    join_c_p_num = r.set("acti_c%d_p%d_num"%(cid, pid),"0")
    jcost_a_c_p_amount = r.set("acti_c%d_p%d_amount"%(cid, pid),"0.0")
    return 1

def del_multiActi_value(cid,pid,hid,uid):
    nodes = [{"host": "192.168.232.14", "port": "5233"}]
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    keys = ["acti_c%d_num"%cid, "acti_c%d_u%d_num"%(cid, uid), "acti_c%d_h%d_num"%(cid, hid), "acti_c%d_h%d_u%d_num"%(cid, hid, uid), "acti_c%d_amount"%cid, "acti_c%d_p%d_num"%(cid, pid), "acti_c%d_p%d_amount"%(cid, pid)]
    for cnt in range(0,6):
        r.delete(keys[cnt])
    return
