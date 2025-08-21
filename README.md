##SOSIM - Solana validator Simulation
#Run:sudo ./sosim.py [hosts_amount] [loss_percentage]

#ARGS:
- hosts amount is for clients amount
- loss_percentage is the same for all links

#Description and notes:
- This simulation runs Solana's mock server and clients (originally implemented by KirillLykov:https://github.com/KirillLykov/mock-server-solana),  customized with logging logic by KOROBYAKA(a.k.a. AlekseiZuev).
- All entities are located in separated namespaces and connected via single 10.0.1.0/24 subnet, all client nodes have a direct connection to the server namespace.
- For cleaning namespaces run "./delete_namespaces", BE CAREFULL IT DELETES ALL NAMESPACES AT THE SCOPE!!!
- Run 'ip netns exec client $TARGET bash' to start a shell in namespace for accessing client/server namespace
- Internet access is not configured inside the namespaces
