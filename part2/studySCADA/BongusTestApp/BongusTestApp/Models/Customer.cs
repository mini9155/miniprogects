﻿using System;
using System.Collections.Generic;

namespace BongusTestApp.Models
{
    public class Customer
    {
        public Guid Id { get; set; }
        public string Name { get; set; }
        public string Address { get; set; }
        public string Phone { get; set; }
        public string ContactName { get; set; }
        public IEnumerable<Order>Orders { get; set; } // 주문한 리스트
    }
}
