using Bogus;
using System;
using System.Collections.Generic;
using System.Linq;

namespace BongusTestApp.Models
{
    public class SampleCustomerRepository
    {
        public IEnumerable<Customer> GetCustomers(int genNum)
        {
            Randomizer.Seed = new Random(123456); // Seed 갯수를 지정, 맘대로
            // 아래와 같은 규칙으로 주문 더미데이터를 생성하겠다
            var orderGen = new Faker<Order>().RuleFor(g => g.Id, Guid.NewGuid)
                                             .RuleFor(d => d.Date, f => f.Date.Past(3))
                                             .RuleFor(o => o.OrderValue, f => f.Finance.Amount(1, 100000))  //ID값은 GUID로 자동생성
                                             .RuleFor(o => o.Shipped, f => f.Random.Bool(0.8f));

            // 고객 더미데이터 생성 규칙
            var customerGen = new Faker<Customer>()
                .RuleFor(c => c.Id, Guid.NewGuid())
                .RuleFor(c => c.Name, f => f.Company.CompanyName())
                .RuleFor(c => c.Address, f => f.Address.FullAddress())
                .RuleFor(c => c.Phone, f => f.Name.FullName())
                .RuleFor(c => c.Orders, f => orderGen.Generate(f.Random.Number(1, 2)).ToList());

            return customerGen.Generate(genNum);
         }
    }
}

