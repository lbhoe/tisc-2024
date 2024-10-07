# Level 4: AlligatorPay

## Description
>In the dark corners of the internet, whispers of an elite group of hackers aiding our enemies have surfaced. The word on the street is that a good number of members from the elite group happens to be part of an exclusive member tier within AlligatorPay (agpay), a popular payment service.
>
>Your task is to find a way to join this exclusive member tier within AlligatorPay and give us intel on future cyberattacks. AlligatorPay recently launched an online balance checker for their payment cards. We heard it's still in beta, so maybe you might find something useful.
>
>Link: https://agpay.chals.tisc24.ctf.sg/

## Solution
Vist the Online Balance Checker.

![image](../images/238eba1716568845da9a5e5e1524c48401009a7cf359021f2bac9e344ab768bb.jpg)  

Observed `ad.gif`.

![image](../images/9bcd0978ee5cefcc3695eade4a040755b0280f530f3a2fa66e4898e6ebb78e10.jpg)  

![image](../images/9713328b01ad4e781cf5d9f5ee62e80bf7582c6b58b1b8675072ce07ee9f734b.jpg)  

`View page source` in browser. Noticed the following comments.

```
---redacted---
      <!-- banner advertisement for AGPay Exclusive Club promo for customers with exactly $313371337 balance -->
---redacted---
      <!-- Dev note: test card for agpay integration can be found at /testcard.agpay  -->
---redacted---
```

Downloaded `testcard.agpay` from  https://agpay.chals.tisc24.ctf.sg/testcard.agpay.

Uploaded `testcard.agpay` to Online Balance Checker.

![image](../images/0b2451d3c1613c318f329ba3e40b0c15460f544bb6df9b74d7651a864f64f66f.jpg)  

Study the functions within `<script>---redacted---</script>` of [page source](./level-4-viewpagesource.txt). Write python script using ChatGPT to create `newcard.agpay` with exactly $313371337 balance. Script can be found [here](./level-4-solution.py).

Uploaded `newcard.agpay` to Online Balance Checker.

![image](../images/f1f6d3c2dc8f271628ed1865b6487a89c6e5b41c17bf396a9dbcede331c3cbaf.jpg)  

## Flag
`TISC{533_Y4_L4T3R_4LL1G4T0R_a8515a1f7004dbf7d5f704b7305cdc5d}`