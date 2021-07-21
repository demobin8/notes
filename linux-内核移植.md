> 做内核移植，刚毕业那会嵌入式很火的。。。

```
Uncompressing Linux... done, booting the kernel.
```
u-boot引导后到这停止了，内核启动不起来，多数是因为u-boot传递的参数不正确造成的，我第一个错误是，OMAP的输出为ttyS2改成ttyO2

打开内核调试

```
kernel hack-->debug earlyprintk

show timing information on printk
```
日志

```
Uncompressing Linux... done, booting the kernel.
[    0.000000] Linux version 3.0.0-rc5brose-g0e90ed0-dirty () (gcc version 4.5.2 (Sourcery G++ Lite 2011.03-41) ) #2 SMP Sun Apr 15 02:15:22 CST 2012
[    0.000000] CPU: ARMv7 Processor [411fc092] revision 2 (ARMv7), cr=10c53c7f
[    0.000000] CPU: VIPT nonaliasing data cache, VIPT aliasing instruction cache
[    0.000000] Machine: OMAP4 Panda board
[    0.000000] bootconsole [earlycon0] enabled
[    0.000000] Reserving 33554432 bytes SDRAM for VRAM
[    0.000000] Memory policy: ECC disabled, Data cache writealloc
[    0.000000] OMAP4430 ES2.2
[    0.000000] SRAM: Mapped pa 0x40300000 to va 0xfe400000 size: 0xe000
[    0.000000] powerdomain: waited too long for powerdomain dss_pwrdm to complete transition
[    0.000000] PERCPU: Embedded 7 pages/cpu @c10ec000 s7040 r8192 d13440 u32768
[    0.000000] Unhandled fault: alignment exception (0x001) at 0xc068ff5a
[    0.000000] Internal error: : 1 [#1] SMP
[    0.000000] Modules linked in:
[    0.000000] CPU: 0    Not tainted  (3.0.0-rc5brose-g0e90ed0-dirty #2)
[    0.000000] PC is at pcpu_dump_alloc_info+0xc/0x248
[    0.000000] LR is at pcpu_setup_first_chunk+0x49c/0x78c
[    0.000000] pc : [<c011dd10>]    lr : [<c00203a8>]    psr: 200001d3
[    0.000000] sp : c074bed8  ip : 00000002  fp : 00008000
[    0.000000] r10: c10f3000  r9 : c10fb040  r8 : c10fb020
[    0.000000] r7 : c07606a4  r6 : c10ec000  r5 : 00003480  r4 : c10e9140
[    0.000000] r3 : c068ff5a  r2 : 00000004  r1 : c10e9140  r0 : c0690241
[    0.000000] Flags: nzCv  IRQs off  FIQs off  Mode SVC_32  ISA ARM  Segment kernel
[    0.000000] Control: 10c53c7f  Table: 8000404a  DAC: 00000017
[    0.000000] Process swapper (pid: 0, stack limit = 0xc074a2f8)
[    0.000000] Stack: (0xc074bed8 to 0xc074c000)
```
 

加入下面这个参数编译

`EXTRA_CFLAGS=-mno-unaligned-access`
