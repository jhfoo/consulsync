# community
import consul

def getConsul(server):
  con = consul.Consul(
    host = server
  )
  return con
