#ifndef PPRODS_H
#define PPRODS_H

// This file is auto-generated by gen_pprods.py

// The array contains products of consecutive odd prime numbers grouped so that
// each product fits into 64 bits.
static const uint64_t pprods[] = {
    0xe221f97c30e94e1d,  // 3*5*7*11*13*17*19*23*29*31*37*41*43*47*53
    0x6329899ea9f2714b,  // 59*61*67*71*73*79*83*89*97*101
    0x58edcb4c9ed39c8b,  // 103*107*109*113*127*131*137*139*149
    0x9966ff94fd516fb,   // 151*157*163*167*173*179*181*191
    0x3bd7632c1f36eb51,  // 193*197*199*211*223*227*229*233
    0xfd14b3c90d88a9,    // 239*241*251*257*263*269*271
    0x2ad3dbe0cca85ff,   // 277*281*283*293*307*311*313
    0x787f9a02c3388a7,   // 317*331*337*347*349*353*359
    0x1113c5cc6d101657,  // 367*373*379*383*389*397*401
    0x2456c94f936bdb15,  // 409*419*421*431*433*439*443
    0x4236a30b85ffe139,  // 449*457*461*463*467*479*487
    0x805437b38eada69d,  // 491*499*503*509*521*523*541
    0x723e97bddcd2af,    // 547*557*563*569*571*577
    0xa5a792ee239667,    // 587*593*599*601*607*613
    0xe451352ebca269,    // 617*619*631*641*643*647
    0x13a7955f14b7805,   // 653*659*661*673*677*683
    0x1d37cbd653b06ff,   // 691*701*709*719*727*733
    0x288fe4eca4d7cdf,   // 739*743*751*757*761*769
    0x39fddb60d3af63d,   // 773*787*797*809*811*821
    0x4cd73f19080fb03,   // 823*827*829*839*853*857
    0x639c390b9313f05,   // 859*863*877*881*883*887
    0x8a1c420d25d388f,   // 907*911*919*929*937*941
    0xb4b5322977db499,   // 947*953*967*971*977*983
    0xe94c170a802ee29,   // 991*997*1009*1013*1019*1021
    0x11f6a0e8356100df,  // 1031*1033*1039*1049*1051*1061
    0x166c8898f7b3d683,  // 1063*1069*1087*1091*1093*1097
    0x1babda0a0afd724b,  // 1103*1109*1117*1123*1129*1151
    0x2471b07c44024abf,  // 1153*1163*1171*1181*1187*1193
    0x2d866dbc2558ad71,  // 1201*1213*1217*1223*1229*1231
    0x3891410d45fb47df,  // 1237*1249*1259*1277*1279*1283
    0x425d5866b049e263,  // 1289*1291*1297*1301*1303*1307
    0x51f767298e2cf13b,  // 1319*1321*1327*1361*1367*1373
    0x6d9f9ece5fc74f13,  // 1381*1399*1409*1423*1427*1429
    0x7f5ffdb0f56ee64d,  // 1433*1439*1447*1451*1453*1459
    0x943740d46a1bc71f,  // 1471*1481*1483*1487*1489*1493
    0xaf2d7ca25cec848f,  // 1499*1511*1523*1531*1543*1549
    0xcec010484e4ad877,  // 1553*1559*1567*1571*1579*1583
    0xef972c3cfafbcd25,  // 1597*1601*1607*1609*1613*1619
    0x2a442c1ebb3be5,    // 1621*1627*1637*1657*1663
    0x303fa164bdc919,    // 1667*1669*1693*1697*1699
    0x36521ca14fd8e7,    // 1709*1721*1723*1733*1741
    0x3ca3241ed069e3,    // 1747*1753*1759*1777*1783
    0x43885d3035c59b,    // 1787*1789*1801*1811*1823
    0x4e1aee1fa9d559,    // 1831*1847*1861*1867*1871
    0x54469dbe5d6c77,    // 1873*1877*1879*1889*1901
    0x5e49791f7429a1,    // 1907*1913*1931*1933*1949
    0x6b2ceda4198e53,    // 1951*1973*1979*1987*1993
    0x7339d26e3d1ce3,    // 1997*1999*2003*2011*2017
    0x7e2ee3b8aa6bf3,    // 2027*2029*2039*2053*2063
    0x8ae9bb5cda9301,    // 2069*2081*2083*2087*2089
    0x96e917373cdca7,    // 2099*2111*2113*2129*2131
    0xa211e4fecdf953,    // 2137*2141*2143*2153*2161
    0xb8ff2efb3033cf,    // 2179*2203*2207*2213*2221
    0xcbaca970bdfe31,    // 2237*2239*2243*2251*2267
    0xdb2c9f75b49027,    // 2269*2273*2281*2287*2293
    0xed9fb524fe759d,    // 2297*2309*2311*2333*2339
    0x1007595a2312fc7,   // 2341*2347*2351*2357*2371
    0x111eccd0898675f,   // 2377*2381*2383*2389*2393
    0x12546177b06c0bf,   // 2399*2411*2417*2423*2437
    0x13e5b450710a16f,   // 2441*2447*2459*2467*2473
    0x164d74c38c8e863,   // 2477*2503*2521*2531*2539
    0x1836887063c20bb,   // 2543*2549*2551*2557*2579
    0x1ab250719364c7b,   // 2591*2593*2609*2617*2621
    0x1d1d99745c88d5b,   // 2633*2647*2657*2659*2663
    0x1ec730b953d1a27,   // 2671*2677*2683*2687*2689
    0x2021f7b6341a9ab,   // 2693*2699*2707*2711*2713
    0x21e792f0d4ca61d,   // 2719*2729*2731*2741*2749
    0x249015c16a93885,   // 2753*2767*2777*2789*2791
    0x26f0f9a480c48e5,   // 2797*2801*2803*2819*2833
    0x29bc3143b9a5a89,   // 2837*2843*2851*2857*2861
    0x2d26abb44109333,   // 2879*2887*2897*2903*2909
    0x30a7492f008069d,   // 2917*2927*2939*2953*2957
    0x343b19b9edc33a7,   // 2963*2969*2971*2999*3001
    0x385a3fb2c68b433,   // 3011*3019*3023*3037*3041
    0x3c555b3dbe9ef83,   // 3049*3061*3067*3079*3083
    0x411e43a3a8d394b,   // 3089*3109*3119*3121*3137
    0x4775710b7a55833,   // 3163*3167*3169*3181*3187
    0x4b76972a22d55a1,   // 3191*3203*3209*3217*3221
    0x507bfe226ee0079,   // 3229*3251*3253*3257*3259
    0x56a838dee32fff3,   // 3271*3299*3301*3307*3313
    0x5ac8589165200e9,   // 3319*3323*3329*3331*3343
    0x5f667749eb2f963,   // 3347*3359*3361*3371*3373
    0x65dd3fc17e3c099,   // 3389*3391*3407*3413*3433
    0x6e031d955a9fef9,   // 3449*3457*3461*3463*3467
    0x742ec64b53bfdff,   // 3469*3491*3499*3511*3517
    0x7a5cbcb6bae243d,   // 3527*3529*3533*3539*3541
    0x7f7fcb28a3d7137,   // 3547*3557*3559*3571*3581
    0x86be427bf5de82d,   // 3583*3593*3607*3613*3617
    0x8d9ca434d0399a5,   // 3623*3631*3637*3643*3659
    0x9638c123bcab351,   // 3671*3673*3677*3691*3697
    0x9db5cdd2505eabd,   // 3701*3709*3719*3727*3733
    0xa7882ea2d1e207f,   // 3739*3761*3767*3769*3779
    0xb1a70a51fba0b75,   // 3793*3797*3803*3821*3823
    0xbbabeb6f4cc2177,   // 3833*3847*3851*3853*3863
    0xc68a56113938121,   // 3877*3881*3889*3907*3911
    0xce86607deddbe4b,   // 3917*3919*3923*3929*3931
    0xdaca6d46347064f,   // 3943*3947*3967*3989*4001
    0xe6f9cb2334ec11f,   // 4003*4007*4013*4019*4021
    0xf25ac800485a171,   // 4027*4049*4051*4057*4073
    0xff8f0253a89a32d,   // 4079*4091*4093*4099*4111
    0x10ccedf304c329c1,  // 4127*4129*4133*4139*4153
    0x11bab365a0306ad1,  // 4157*4159*4177*4201*4211
    0x12bc79f95534c5d9,  // 4217*4219*4229*4231*4241
    0x136918855651cae7,  // 4243*4253*4259*4261*4271
    0x1441022b5202f195,  // 4273*4283*4289*4297*4327
    0x1597271595caf351,  // 4337*4339*4349*4357*4363
    0x16d6d391503c0abb,  // 4373*4391*4397*4409*4421
    0x180c60c57c2aa2eb,  // 4423*4441*4447*4451*4457
    0x1931ed2425952793,  // 4463*4481*4483*4493*4507
    0x1a4ad806a56da143,  // 4513*4517*4519*4523*4547
    0x1bab1dcc65ac15db,  // 4549*4561*4567*4583*4591
    0x1d309fb6e722f0e1,  // 4597*4603*4621*4637*4639
    0x1e414485a1b107bf,  // 4643*4649*4651*4657*4663
    0x1f9aa68df17c076b,  // 4673*4679*4691*4703*4721
    0x212b81780b580e97,  // 4723*4729*4733*4751*4759
    0x23006478f7a04647,  // 4783*4787*4789*4793*4799
    0x244664b9e9752837,  // 4801*4813*4817*4831*4861
    0x26cb4c8923562f31,  // 4871*4877*4889*4903*4909
    0x2885c6c7b07c160f,  // 4919*4931*4933*4937*4943
    0x29cdb8dbe624c3c1,  // 4951*4957*4967*4969*4973
    0x2b4a321722f3b1ef,  // 4987*4993*4999*5003*5009
    0x2ca3b94e7373f36d,  // 5011*5021*5023*5039*5051
    0x2efa302d0838fad3,  // 5059*5077*5081*5087*5099
    0x30b3fdb20c872a5b,  // 5101*5107*5113*5119*5147
    0x33591223fefd974b,  // 5153*5167*5171*5179*5189
    0x35c12a863f50eaa9,  // 5197*5209*5227*5231*5233
    0x383533808bd74477,  // 5237*5261*5273*5279*5281
    0x3ac02a15fc89c54d,  // 5297*5303*5309*5323*5333
    0x3e12cc83606624f3,  // 5347*5351*5381*5387*5393
    0x405f92575cd90b87,  // 5399*5407*5413*5417*5419
    0x42211307d533e619,  // 5431*5437*5441*5443*5449
    0x44b8a22c7f3df3c3,  // 5471*5477*5479*5483*5501
    0x46d3dca711bbaec5,  // 5503*5507*5519*5521*5527
    0x49a4f62f2bee3201,  // 5531*5557*5563*5569*5573
    0x4d746a3fda9d6ec3,  // 5581*5591*5623*5639*5641
    0x5024bb19621ceac3,  // 5647*5651*5653*5657*5659
    0x528d8d1989f23337,  // 5669*5683*5689*5693*5701
    0x55b4c3f0688fa659,  // 5711*5717*5737*5741*5743
    0x599291b29311407f,  // 5749*5779*5783*5791*5801
    0x5cc7a1b4f6df9823,  // 5807*5813*5821*5827*5839
    0x5f42cbfa215ab3fd,  // 5843*5849*5851*5857*5861
    0x616db4fe760c22b9,  // 5867*5869*5879*5881*5897
    0x65ad151b5817da41,  // 5903*5923*5927*5939*5953
    0x6c2e75f079f3deef,  // 5981*5987*6007*6011*6029
    0x706dd813a4085937,  // 6037*6043*6047*6053*6067
    0x73edc48854faa299,  // 6073*6079*6089*6091*6101
    0x77f1e576ffed49b9,  // 6113*6121*6131*6133*6143
    0x7cc13fe542982693,  // 6151*6163*6173*6197*6199
    0x80cedb56d0c02049,  // 6203*6211*6217*6221*6229
    0x858f4783e6ff5cf3,  // 6247*6257*6263*6269*6271
    0x892e6d86008f82e3,  // 6277*6287*6299*6301*6311
    0x8d040c52d7c6ab79,  // 6317*6323*6329*6337*6343
    0x90b53592209da955,  // 6353*6359*6361*6367*6373
    0x954fb9d96ab9ea1d,  // 6379*6389*6397*6421*6427
    0x9caf15af4ce7fcf7,  // 6449*6451*6469*6473*6481
    0xa47dbf171698939f,  // 6491*6521*6529*6547*6551
    0xa9712f0456e54591,  // 6553*6563*6569*6571*6577
    0xaeed828a42377403,  // 6581*6599*6607*6619*6637
    0xb68603f5eadb8545,  // 6653*6659*6661*6673*6679
    0xbb2bd5d42428b71d,  // 6689*6691*6701*6703*6709
    0xc165b45b4e412e49,  // 6719*6733*6737*6761*6763
    0xc8348a8471e75ca3,  // 6779*6781*6791*6793*6803
    0xce5ab711e7179571,  // 6823*6827*6829*6833*6841
    0xd4287981935f5b7f,  // 6857*6863*6869*6871*6883
    0xdb9c1eff1b938a91,  // 6899*6907*6911*6917*6947
    0xe2e20afc369136ff,  // 6949*6959*6961*6967*6971
    0xe78c749d7a119695,  // 6977*6983*6991*6997*7001
    0xedfa86764fa767e1,  // 7013*7019*7027*7039*7043
    0xf7780828d01fcef9,  // 7057*7069*7079*7103*7109
    0x9311da8eb3ea1,     // 7121*7127*7129*7151
    0x96fc1b51999b5,     // 7159*7177*7187*7193
    0x99d2dc5aa820b,     // 7207*7211*7213*7219
    0x9c18c1a21f755,     // 7229*7237*7243*7247
    0xa019a0d84ce05,     // 7253*7283*7297*7307
    0xa3837104af50b,     // 7309*7321*7331*7333
    0xa74ba276e925b,     // 7349*7351*7369*7393
    0xad0c05b3ae661,     // 7411*7417*7433*7451
    0xb0da5211cc3e7,     // 7457*7459*7477*7481
    0xb36ca8c3991af,     // 7487*7489*7499*7507
    0xb6694790c60df,     // 7517*7523*7529*7537
    0xb89a345c48d7d,     // 7541*7547*7549*7559
    0xbb02a8b8a132b,     // 7561*7573*7577*7583
    0xbd6468bb171ff,     // 7589*7591*7603*7607
    0xc17671b548641,     // 7621*7639*7643*7649
    0xc57f07d496e1b,     // 7669*7673*7681*7687
    0xc814b88200ac3,     // 7691*7699*7703*7717
    0xcb958ba8e9259,     // 7723*7727*7741*7753
    0xcfaa956d67517,     // 7757*7759*7789*7793
    0xd56380a0e8273,     // 7817*7823*7829*7841
    0xd9c8b65d94f5b,     // 7853*7867*7873*7877
    0xdc90a482debcb,     // 7879*7883*7901*7907
    0xe0ac9922e6235,     // 7919*7927*7933*7937
    0xe4aa6969c4449,     // 7949*7951*7963*7993
    0xeb0ca4d2b0965,     // 8009*8011*8017*8039
    0xf08c969789d43,     // 8053*8059*8069*8081
    0xf3c97c77c730f,     // 8087*8089*8093*8101
    0xf7aa31273931b,     // 8111*8117*8123*8147
    0xfd32e0bae7a77,     // 8161*8167*8171*8179
    0x102419fda6cc01,    // 8191*8209*8219*8221
    0x1058b57cd1fec9,    // 8231*8233*8237*8243
    0x10a468ac696a55,    // 8263*8269*8273*8287
    0x10d824894d6521,    // 8291*8293*8297*8311
    0x1131219641c957,    // 8317*8329*8353*8363
    0x1186346cb9c4a7,    // 8369*8377*8387*8389
    0x11e75887c6bcbf,    // 8419*8423*8429*8431
    0x1226c3d8919ad3,    // 8443*8447*8461*8467
    0x12ae54ca9118b3,    // 8501*8513*8521*8527
    0x12f2143ddeb927,    // 8537*8539*8543*8563
    0x13522200caeeb3,    // 8573*8581*8597*8599
    0x13a21ad000a461,    // 8609*8623*8627*8629
    0x13ef7c7f69a93d,    // 8641*8647*8663*8669
    0x1436a05ef17841,    // 8677*8681*8689*8693
    0x147142f4cc4c17,    // 8699*8707*8713*8719
    0x14b887295ec96d,    // 8731*8737*8741*8747
    0x1501b9fe3efaad,    // 8753*8761*8779*8783
    0x156d3ebd5cfffb,    // 8803*8807*8819*8821
    0x15af86361077ad,    // 8831*8837*8839*8849
    0x15fc898c07b90f,    // 8861*8863*8867*8887
    0x167c836a7cdf2b,    // 8893*8923*8929*8933
    0x16db56bc574209,    // 8941*8951*8963*8969
    0x174097de2edf3b,    // 8971*8999*9001*9007
    0x178dbdb0cfb9fb,    // 9011*9013*9029*9041
    0x17e109fd2af3fb,    // 9043*9049*9059*9067
    0x18716adbb946f7,    // 9091*9103*9109*9127
    0x18d7bc2e97eaef,    // 9133*9137*9151*9157
    0x192e69d59ba8db,    // 9161*9173*9181*9187
    0x198a3cddb561c9,    // 9199*9203*9209*9221
    0x19e876c274e4fd,    // 9227*9239*9241*9257
    0x1a63555c2e680b,    // 9277*9281*9283*9293
    0x1ad58f177dacbb,    // 9311*9319*9323*9337
    0x1b29f0db4b3395,    // 9341*9343*9349*9371
    0x1ba4b691e66139,    // 9377*9391*9397*9403
    0x1bfc87fc12613d,    // 9413*9419*9421*9431
    0x1c3e250dac9d87,    // 9433*9437*9439*9461
    0x1c944c9149df3b,    // 9463*9467*9473*9479
    0x1cff79f4c205cd,    // 9491*9497*9511*9521
    0x1d75566cb1adb3,    // 9533*9539*9547*9551
    0x1e3cd7b5975575,    // 9587*9601*9613*9619
    0x1e92a4033b7417,    // 9623*9629*9631*9643
    0x1f0502cb33d8c7,    // 9649*9661*9677*9679
    0x1f8943169b2d87,    // 9689*9697*9719*9721
    0x1ffcaebc1a4bad,    // 9733*9739*9743*9749
    0x20730086c8cb89,    // 9767*9769*9781*9787
    0x20d7b89585d217,    // 9791*9803*9811*9817
    0x2147bfe14a8231,    // 9829*9833*9839*9851
    0x21ae6440d699bf,    // 9857*9859*9871*9883
    0x22306f8188c6fb,    // 9887*9901*9907*9923
    0x22a5af39a69703,    // 9929*9931*9941*9949
    0x235eedc5de5805,    // 9967*9973*10007*10009
    0x2441e04ba35085,    // 10037*10039*10061*10067
    0x24b8a97a3a59a5,    // 10069*10079*10091*10093
    0x252362655a4d67,    // 10099*10103*10111*10133
    0x25ab86b8cc3567,    // 10139*10141*10151*10159
    0x260aea245bc247,    // 10163*10169*10177*10181
    0x26b855f8b70077,    // 10193*10211*10223*10243
    0x2750993dd1e65b,    // 10247*10253*10259*10267
    0x27bafa8c9f7853,    // 10271*10273*10289*10301
    0x28402b9d2d22dd,    // 10303*10313*10321*10331
    0x28a66d2d4fc087,    // 10333*10337*10343*10357
    0x298166c0739b53,    // 10369*10391*10399*10427
    0x2a40d5220cbed9,    // 10429*10433*10453*10457
    0x2ab7670bbab197,    // 10459*10463*10477*10487
    0x2b5b38f61706df,    // 10499*10501*10513*10529
    0x2c3429fa1e037f,    // 10531*10559*10567*10589
    0x2ceda9fa3b4a9f,    // 10597*10601*10607*10613
    0x2d7b4d561f2739,    // 10627*10631*10639*10651
    0x2e05d3caae9813,    // 10657*10663*10667*10687
    0x2eb7851a14c29b,    // 10691*10709*10711*10723
    0x2f3e1d077d25cf,    // 10729*10733*10739*10753
    0x3010f41dbeb6ed,    // 10771*10781*10789*10799
    0x311729b61dd159,    // 10831*10837*10847*10853
    0x318dceb77a5837,    // 10859*10861*10867*10883
    0x321cd33785cdf1,    // 10889*10891*10903*10909
    0x32fdf49691bc63,    // 10937*10939*10949*10957
    0x33b1c5f5f30ced,    // 10973*10979*10987*10993
    0x34a6c59cb6d8d7,    // 11003*11027*11047*11057
    0x355c9029e55dd3,    // 11059*11069*11071*11083
    0x35fb2d1ac371b7,    // 11087*11093*11113*11117
    0x36b44bc2249a47,    // 11119*11131*11149*11159
    0x3750e273f3b60f,    // 11161*11171*11173*11177
    0x385ce9399c0f85,    // 11197*11213*11239*11243
    0x391ecbd93a9e67,    // 11251*11257*11261*11273
    0x39cd91131ee8e5,    // 11279*11287*11299*11311
    0x3a887d9033256b,    // 11317*11321*11329*11351
    0x3b77f83e7b7b77,    // 11353*11369*11383*11393
    0x3c5f7ed2eca1bf,    // 11399*11411*11423*11437
    0x3d367feec26269,    // 11443*11447*11467*11471
    0x3debdb2f48a479,    // 11483*11489*11491*11497
    0x3eab0afe5d537b,    // 11503*11519*11527*11549
    0x3fd435f4d431e7,    // 11551*11579*11587*11593
    0x40b45ff452cb31,    // 11597*11617*11621*11633
    0x420775fbceaf6d,    // 11657*11677*11681*11689
    0x42c7627aefc08d,    // 11699*11701*11717*11719
    0x43e44dcc615d67,    // 11731*11743*11777*11779
    0x44c330cdfdeb7d,    // 11783*11789*11801*11807
    0x456af335c23b75,    // 11813*11821*11827*11831
    0x4610d2c7c0027b,    // 11833*11839*11863*11867
    0x47384e9bf4bfad,    // 11887*11897*11903*11909
    0x47fa259c013ba3,    // 11923*11927*11933*11939
    0x48950fc7f50b43,    // 11941*11953*11959*11969
    0x4956836a576163,    // 11971*11981*11987*12007
    0x4a7b8c3c557b65,    // 12011*12037*12041*12043
    0x4b771e5db917ef,    // 12049*12071*12073*12097
    0x4c5834105e9dfb,    // 12101*12107*12109*12113
    0x4d37df06ec25d9,    // 12119*12143*12149*12157
    0x4e3707bf47eca5,    // 12161*12163*12197*12203
    0x4f77e5a59ceea7,    // 12211*12227*12239*12241
    0x503ced574122d5,    // 12251*12253*12263*12269
    0x50f93a4e9e43e9,    // 12277*12281*12289*12301
    0x5242764cb96dbf,    // 12323*12329*12343*12347
    0x5373ff17a4f379,    // 12373*12377*12379*12391
    0x544ac8e491c7d9,    // 12401*12409*12413*12421
    0x5534b35cc8f027,    // 12433*12437*12451*12457
    0x56405cd1d8f29b,    // 12473*12479*12487*12491
    0x56ee39496a06dd,    // 12497*12503*12511*12517
    0x57cf4552f1e303,    // 12527*12539*12541*12547
    0x58b59c4b50c127,    // 12553*12569*12577*12583
    0x59a507c3dbf24b,    // 12589*12601*12611*12613
    0x5a92a6fbea27b9,    // 12619*12637*12641*12647
    0x5b7e66124ac799,    // 12653*12659*12671*12689
    0x5cab65d44446ef,    // 12697*12703*12713*12721
    0x5de6905c90b503,    // 12739*12743*12757*12763
    0x5f37e803c461fd,    // 12781*12791*12799*12809
    0x60383597fe3f4f,    // 12821*12823*12829*12841
    0x61e147bd94922b,    // 12853*12889*12893*12899
    0x62cb93e709f30f,    // 12907*12911*12917*12919
    0x63bb5109ddbb39,    // 12923*12941*12953*12959
    0x64b4ccd52a2a97,    // 12967*12973*12979*12983
    0x65a00fb544939d,    // 13001*13003*13007*13009
    0x66bd48d7520557,    // 13033*13037*13043*13049
    0x684ac380bf1aaf,    // 13063*13093*13099*13103
    0x6975d3e0fb99e1,    // 13109*13121*13127*13147
    0x6a96fad34eb5c9,    // 13151*13159*13163*13171
    0x6b9092527de0b5,    // 13177*13183*13187*13217
    0x6cfda2f8b38f6f,    // 13219*13229*13241*13249
    0x6e72811aacaeab,    // 13259*13267*13291*13297
    0x6fd5b0d3d77ca9,    // 13309*13313*13327*13331
    0x710c5f58855659,    // 13337*13339*13367*13381
    0x72c045f81a9571,    // 13397*13399*13411*13417
    0x740178628c8d1f,    // 13421*13441*13451*13457
    0x7518d8f35a1ee9,    // 13463*13469*13477*13487
    0x76a24bc5928fc9,    // 13499*13513*13523*13537
    0x788a7d5fa3bc21,    // 13553*13567*13577*13591
    0x7a0a454ddc12d9,    // 13597*13613*13619*13627
    0x7b9b6dbf0acbfb,    // 13633*13649*13669*13679
    0x7cb724b29c97e9,    // 13681*13687*13691*13693
    0x7d80316c3aea0b,    // 13697*13709*13711*13721
    0x7e9f02956774f9,    // 13723*13729*13751*13757
    0x7fd78ff30e55dd,    // 13759*13763*13781*13789
    0x8176f93dcdee1b,    // 13799*13807*13829*13831
    0x83328f181f37ff,    // 13841*13859*13873*13877
    0x844c85844f1ec7,    // 13879*13883*13901*13903
    0x854fb5954cd2e9,    // 13907*13913*13921*13931
    0x871ee1f72316ed,    // 13933*13963*13967*13997
    0x88f30d5a797dc9,    // 13999*14009*14011*14029
    0x8a8f2c1377c21d,    // 14033*14051*14057*14071
    0x8c01286e805837,    // 14081*14083*14087*14107
    0x8e7712e261c25d,    // 14143*14149*14153*14159
    0x8ffb253ef4179f,    // 14173*14177*14197*14207
    0x921fbe50feef75,    // 14221*14243*14249*14251
    0x948a2d689dccf3,    // 14281*14293*14303*14321
    0x95ffe36390e923,    // 14323*14327*14341*14347
    0x98301d5150c82f,    // 14369*14387*14389*14401
    0x9965ca922eda71,    // 14407*14411*14419*14423
    0x9a81df9eec8585,    // 14431*14437*14447*14449
    0x9c4ff7ceb26e9d,    // 14461*14479*14489*14503
    0x9e7b7d2e8d6945,    // 14519*14533*14537*14543
    0x9f6c20cfec7617,    // 14549*14551*14557*14561
    0xa1123741d60349,    // 14563*14591*14593*14621
    0xa2d85d546633e9,    // 14627*14629*14633*14639
    0xa4576a38b2e863,    // 14653*14657*14669*14683
    0xa67b26cfff14d5,    // 14699*14713*14717*14723
    0xa7a939b6101c2d,    // 14731*14737*14741*14747
    0xa8bb9c6b89238b,    // 14753*14759*14767*14771
    0xaa21a4d7b7405d,    // 14779*14783*14797*14813
    0xabdd00ad8a3843,    // 14821*14827*14831*14843
    0xad89beafbcecf3,    // 14851*14867*14869*14879
    0xaf157a9999de1f,    // 14887*14891*14897*14923
    0xb1110edec9a5e7,    // 14929*14939*14947*14951
};
#endif // PPRODS_H
