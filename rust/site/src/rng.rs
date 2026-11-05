//! Python's random.Random: MT19937 with its seeding and its derived draws, so a seed gives what it
//! always gave. Shared by the site crate (each page's plate) and the bot (/name, /stats).

/// random.Random: MT19937 with Python's seeding and its derived draws.
pub struct Random {
    mt: [u32; 624],
    i: usize,
}

impl Random {
    fn from_key(key: &[u32]) -> Self {
        let mut mt = [0u32; 624];
        mt[0] = 19650218;
        for i in 1..624 {
            mt[i] = 1812433253u32.wrapping_mul(mt[i - 1] ^ (mt[i - 1] >> 30)).wrapping_add(i as u32);
        }
        let (mut i, mut j) = (1, 0);
        for _ in 0..624.max(key.len()) {
            mt[i] = (mt[i] ^ (mt[i - 1] ^ (mt[i - 1] >> 30)).wrapping_mul(1664525)).wrapping_add(key[j]).wrapping_add(j as u32);
            i += 1;
            j += 1;
            if i >= 624 {
                mt[0] = mt[623];
                i = 1;
            }
            if j >= key.len() {
                j = 0;
            }
        }
        for _ in 0..623 {
            mt[i] = (mt[i] ^ (mt[i - 1] ^ (mt[i - 1] >> 30)).wrapping_mul(1566083941)).wrapping_sub(i as u32);
            i += 1;
            if i >= 624 {
                mt[0] = mt[623];
                i = 1;
            }
        }
        mt[0] = 0x8000_0000;
        Random { mt, i: 624 }
    }

    /// Random(a big-endian integer): its 32-bit words, least significant first.
    pub fn from_be_bytes(be: &[u8]) -> Self {
        let mut key: Vec<u32> = be.rchunks(4).map(|c| c.iter().fold(0u32, |a, b| (a << 8) | u32::from(*b))).collect();
        while key.len() > 1 && key.last() == Some(&0) {
            key.pop();
        }
        Self::from_key(&key)
    }

    fn next_u32(&mut self) -> u32 {
        if self.i >= 624 {
            for k in 0..624 {
                let y = (self.mt[k] & 0x8000_0000) | (self.mt[(k + 1) % 624] & 0x7fff_ffff);
                self.mt[k] = self.mt[(k + 397) % 624] ^ (y >> 1) ^ if y & 1 == 1 { 0x9908_b0df } else { 0 };
            }
            self.i = 0;
        }
        let mut y = self.mt[self.i];
        self.i += 1;
        y ^= y >> 11;
        y ^= (y << 7) & 0x9d2c_5680;
        y ^= (y << 15) & 0xefc6_0000;
        y ^ (y >> 18)
    }

    pub fn random(&mut self) -> f64 {
        let (a, b) = (self.next_u32() >> 5, self.next_u32() >> 6);
        (f64::from(a) * 67108864.0 + f64::from(b)) / 9007199254740992.0
    }

    pub fn uniform(&mut self, a: f64, b: f64) -> f64 {
        a + (b - a) * self.random()
    }

    pub fn below(&mut self, n: u32) -> u32 {
        let k = 32 - n.leading_zeros();
        loop {
            let r = self.next_u32() >> (32 - k);
            if r < n {
                return r;
            }
        }
    }

    pub fn randint(&mut self, a: i64, b: i64) -> i64 {
        a + i64::from(self.below((b - a + 1) as u32))
    }

    pub fn choice<T: Clone>(&mut self, items: &[T]) -> T {
        items[self.below(items.len() as u32) as usize].clone()
    }

    /// random.sample, both of its branches.
    pub fn sample<T: Clone>(&mut self, items: &[T], k: usize) -> Vec<T> {
        let n = items.len();
        let mut setsize = 21usize;
        if k > 5 {
            setsize += 4usize.pow(((k * 3) as f64).log(4.0).ceil() as u32);
        }
        if n <= setsize {
            let mut pool = items.to_vec();
            return (0..k)
                .map(|i| {
                    let j = self.below((n - i) as u32) as usize;
                    let v = pool[j].clone();
                    pool[j] = pool[n - i - 1].clone();
                    v
                })
                .collect();
        }
        let mut seen = std::collections::HashSet::new();
        (0..k)
            .map(|_| {
                let mut j = self.below(n as u32) as usize;
                while !seen.insert(j) {
                    j = self.below(n as u32) as usize;
                }
                items[j].clone()
            })
            .collect()
    }

    /// random.gammavariate for alpha above 1 (Cheng's method).
    #[allow(dead_code)] // the bot uses it, the site does not
    pub fn gammavariate(&mut self, alpha: f64, beta: f64) -> f64 {
        let (ainv, log4) = ((2.0 * alpha - 1.0).sqrt(), 4.0f64.ln());
        let (bbb, ccc, sg) = (alpha - log4, alpha + ainv, 1.0 + 4.5f64.ln());
        loop {
            let u1 = self.random();
            if !(1e-7 < u1 && u1 < 0.9999999) {
                continue;
            }
            let u2 = 1.0 - self.random();
            let v = (u1 / (1.0 - u1)).ln() / ainv;
            let x = alpha * v.exp();
            let z = u1 * u1 * u2;
            let r = bbb + ccc * v - x;
            if r + sg - 4.5 * z >= 0.0 || r >= z.ln() {
                return x * beta;
            }
        }
    }
}
