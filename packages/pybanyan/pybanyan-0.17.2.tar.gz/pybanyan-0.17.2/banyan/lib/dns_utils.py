# import dns.resolver
# from banyan.model.netagent import Netagent
#
#
# n: Netagent = Netagent.Schema().loads(open("tests/data/netagent.json").read())
#
# resolver = dns.resolver.Resolver(configure=False)
# resolver.nameservers = ['1.1.1.1']
# answers = resolver.resolve('pst.transtar.bnndemos.com', 'A')
# for answer in answers:  # type: dns.resolver.Answer
#     print(answer.address, answer.address in n.ip_addresses)
