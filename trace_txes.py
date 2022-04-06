from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from datetime import datetime

rpc_user='quaker_quorum'
rpc_password='franklin_fought_for_continental_cash'
rpc_ip='3.134.159.30'
rpc_port='8332'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_ip, rpc_port))

###################################

class TXO:
    def __init__(self, tx_hash, n, amount, owner, time ):
        self.tx_hash = tx_hash 
        self.n = n
        self.amount = amount
        self.owner = owner
        self.time = time
        self.inputs = []

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.tx_hash)+"\n"
        for tx in self.inputs:
            ret += tx.__str__(level+1)
        return ret

    def to_json(self):
        fields = ['tx_hash','n','amount','owner']
        json_dict = { field: self.__dict__[field] for field in fields }
        json_dict.update( {'time': datetime.timestamp(self.time) } )
        if len(self.inputs) > 0:
            for txo in self.inputs:
                json_dict.update( {'inputs': json.loads(txo.to_json()) } )
        return json.dumps(json_dict, sort_keys=True, indent=4)

    @classmethod
    def from_tx_hash(cls,tx_hash,n=0):
        #YOUR CODE HERE
        tx = rpc_connection.getrawtransaction(tx_hash,True)
        #print(tx)
        txo = tx.get('vout')[n]
        amount = int(txo.get('value')*pow(10,8))
        owner = txo.get('scriptPubKey').get('addresses')[0]
        time = datetime.fromtimestamp(tx.get('time'))
        return TXO(tx_hash,n,amount,owner,time)
        #pass
        

    def get_inputs(self,d=1):
        tx = rpc_connection.getrawtransaction(self.tx_hash,True)
        parent_id = tx.get('vin')[0].get('txid')
        #print("TX")
        #print(tx)
        #print("tx.vin")
        #print(parent)
        #print("tx.vin.txid.vout")
        tx_get_inputs = TXO.from_tx_hash('1620c59574743195fb5ad0d0bf96ac4e16a78f3912a58d23c6e2aeaf2595bfe7')
        print(rpc_connection.getrawtransaction(tx_get_inputs.tx_hash,True))
        vin_outputs = rpc_connection.getrawtransaction(parent_id,True).get('vout')
        for i in range(len(vin_outputs)):
            self.inputs.append(TXO.from_tx_hash(parent_id,i))
        #print(self.inputs)
        return self.inputs
        #gparent = rpc_connection.getrawtransaction(parents[0].get('txid'),True)
        #self.inputs.append(TXO.from_tx_hash(gparent.get('txid')))
        '''
        for depth in range(d):
            for i in len(parents):
                parent = rpc_connection.getrawtransaction(inputs[i].get('txid'),True)
                for j in range(len(parent.get('vout'))
                    self.inputs.append(from_tx_hash(parent.get('txid'),j))
                
                print(parent)
                for i in range(len(inputs)):
                    txo = tx.get('vin')[i]
                    print(txo)
                    amount = int(txo.get('value')*pow(10,8))
                    owner = txo.get('scriptPubKey').get('hex')
                    time = datetime.fromtimestamp(tx.get('time'))
                    self.inputs.append(TXO(self.tx_hash,i,amount,owner,time)) 
        '''          
        
        pass
        #YOUR CODE HERE


