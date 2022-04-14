# ganache-cli --account="<privatekey>,balance" [--account="<privatekey>,balance"]

# "client_pub" : "0x2e4407268a7890f36cd22dec08e4ce1f6b407492",
# "client_pk" : "0x81d43c5a1d1001308ad5d7691e9f4905925d611910b73a5d01a80ac45db2294f",
# "service_provider_pub" : "0x8a84446da9c74f5937134f1436d734d586f597b4",
# "service_provider_pk" : "0x98751e41b03e2cdccc9111433c8a874016f55899a9add833d5f236d18ffe7343",
# "bank_address" : "0x62B9a2F427Ae8649b2467e08095C65551140926d",
# "bank_private_key" : "4a43f77cc5a1e8e2d1411a272b80dcbb6cfcbb01624553a81c59bd0ef4455efc"

# [--account="<0x98751e41b03e2cdccc9111433c8a874016f55899a9add833d5f236d18ffe7343>,100"]
# 0x56BC75E2D63100000 is 100eth in wei

echo "Launching local blockchain ..."
ganache-cli -i=1337 --account="0x81d43c5a1d1001308ad5d7691e9f4905925d611910b73a5d01a80ac45db2294f,0x56BC75E2D63100000" --account="0x98751e41b03e2cdccc9111433c8a874016f55899a9add833d5f236d18ffe7343,0x56BC75E2D63100000" --account="0x4a43f77cc5a1e8e2d1411a272b80dcbb6cfcbb01624553a81c59bd0ef4455efc,0x56BC75E2D63100000" --blockTime=1