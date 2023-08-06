#!/usr/bin/env python3

import dup_crypto

def test():
	seed_bytes = b"\x80bis\xfb\xcd\x13 \xd2U\xd1\xb9M\xe4\xe8\xc4}\xba\x9f7^z\xe7\xe7\x91\x7f\xecAjj2\x8d"
	seed = dup_crypto.seeds.Seed32(seed_bytes)
	keypair = dup_crypto.keys.ed25519.Keypair.from_seed32(seed)
	
	assert keypair.pubkey.to_base58() == "AoxVA41dGL2s4ogMNdbCw3FFYjFo5FPK36LuiW1tjGbG"
	
	msg = b"Hello world!"
	signator = keypair.signator()
	signature = signator.sign(msg)
	
	assert signator.pubkey == keypair.pubkey
	assert keypair.verify(msg, signature)
	try:
		signature = signature[0:63]+bytes([(signature[63]+1)%256])
		keypair.verify(msg, signature)
		raise Exception("Altered signature verified")
	except ValueError:
		pass
	
	dewif = dup_crypto.dewif.write_dewif(dup_crypto.dewif.CURRENCY_G1_TEST, keypair, 1, "My super passphrase")
	d = dup_crypto.dewif.read_dewif(dewif, "My super passphrase")
	assert len(d) == 1
	assert d[0].pubkey == keypair.pubkey
	d = dup_crypto.dewif.read_dewif(dewif, "My super passphrase", dup_crypto.dewif.CURRENCY_G1_TEST)
	assert len(d) == 1
	assert d[0].pubkey == keypair.pubkey
	dewif = dup_crypto.dewif.change_dewif_passphrase(dewif, "My super passphrase", "Another passphrase")
	d = dup_crypto.dewif.read_dewif(dewif, "Another passphrase")
	assert len(d) == 1
	assert d[0].pubkey == keypair.pubkey
	
	assert dup_crypto.keys.ed25519.Keypair.from_scrypt("a", "b").pubkey.to_base58() == "AoxVA41dGL2s4ogMNdbCw3FFYjFo5FPK36LuiW1tjGbG"
	assert dup_crypto.keys.ed25519.Keypair.from_seed32(dup_crypto.seeds.Seed32.from_scrypt(b"a", b"b")).pubkey.to_base58() == "AoxVA41dGL2s4ogMNdbCw3FFYjFo5FPK36LuiW1tjGbG"
	
	sender = dup_crypto.keys.ed25519.Keypair.random()
	receiver = dup_crypto.keys.ed25519.Keypair.random()
	msg = dup_crypto.private_message.encrypt(b"test", dup_crypto.private_message.ALGO_CHACHA20POLY1305, False, b"Hello world!", receiver.pubkey, sender)
	msg_signed = dup_crypto.private_message.encrypt(b"test", dup_crypto.private_message.ALGO_CHACHA20POLY1305, True, b"Hello world!", receiver.pubkey, sender)
	assert dup_crypto.private_message.decrypt(b"test", dup_crypto.private_message.ALGO_CHACHA20POLY1305, msg, receiver) == (b"Hello world!", sender.pubkey, None)
	c_msg, c_pubkey, c_signature = dup_crypto.private_message.decrypt(b"test", dup_crypto.private_message.ALGO_CHACHA20POLY1305, msg_signed, receiver)
	assert c_msg == b"Hello world!"
	assert c_pubkey == sender.pubkey
	assert sender.pubkey.verify(c_msg, c_signature)
	
	print("All tests OK!")

if __name__ == "__main__":
	test()
