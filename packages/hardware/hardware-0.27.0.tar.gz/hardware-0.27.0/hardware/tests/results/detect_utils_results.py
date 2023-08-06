# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


IPMI_SDR_RESULT = [('ipmi', 'UID Light', 'value', '0x00'),
                   ('ipmi', 'Sys. Health LED', 'value', '0x00'),
                   ('ipmi', 'Power Supply 1', 'value', '90'),
                   ('ipmi', 'Power Supply 1', 'unit', 'Watts'),
                   ('ipmi', 'Power Supply 2', 'value', '65'),
                   ('ipmi', 'Power Supply 2', 'unit', 'Watts'),
                   ('ipmi', 'Power Supplies', 'value', '0x00'),
                   ('ipmi', 'Fan 1', 'value', '33.32'),
                   ('ipmi', 'Fan 1', 'unit', 'percent'),
                   ('ipmi', 'Fan 2', 'value', '39.20'),
                   ('ipmi', 'Fan 2', 'unit', 'percent'),
                   ('ipmi', 'Fan 3', 'value', '39.20'),
                   ('ipmi', 'Fan 3', 'unit', 'percent'),
                   ('ipmi', 'Fan 4', 'value', '29.40'),
                   ('ipmi', 'Fan 4', 'unit', 'percent'),
                   ('ipmi', 'Fan 5', 'value', '24.70'),
                   ('ipmi', 'Fan 5', 'unit', 'percent'),
                   ('ipmi', 'Fan 6', 'value', '13.72'),
                   ('ipmi', 'Fan 6', 'unit', 'percent'),
                   ('ipmi', 'Fans', 'value', '0x00'),
                   ('ipmi', 'Temp 1', 'value', '20'),
                   ('ipmi', 'Temp 1', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 2', 'value', '40'),
                   ('ipmi', 'Temp 2', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 3', 'value', '40'),
                   ('ipmi', 'Temp 3', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 4', 'value', '28'),
                   ('ipmi', 'Temp 4', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 5', 'value', '28'),
                   ('ipmi', 'Temp 5', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 6', 'value', '34'),
                   ('ipmi', 'Temp 6', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 7', 'value', '33'),
                   ('ipmi', 'Temp 7', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 8', 'value', '39'),
                   ('ipmi', 'Temp 8', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 9', 'value', '33'),
                   ('ipmi', 'Temp 9', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 10', 'value', '39'),
                   ('ipmi', 'Temp 10', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 11', 'value', '29'),
                   ('ipmi', 'Temp 11', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 12', 'value', '40'),
                   ('ipmi', 'Temp 12', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 13', 'value', '28'),
                   ('ipmi', 'Temp 13', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 14', 'value', '31'),
                   ('ipmi', 'Temp 14', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 15', 'value', '29'),
                   ('ipmi', 'Temp 15', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 16', 'value', '25'),
                   ('ipmi', 'Temp 16', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 17', 'value', '27'),
                   ('ipmi', 'Temp 17', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 18', 'value', 'disabled'),
                   ('ipmi', 'Temp 19', 'value', '22'),
                   ('ipmi', 'Temp 19', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 20', 'value', '28'),
                   ('ipmi', 'Temp 20', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 21', 'value', '28'),
                   ('ipmi', 'Temp 21', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 22', 'value', '28'),
                   ('ipmi', 'Temp 22', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 23', 'value', '33'),
                   ('ipmi', 'Temp 23', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 24', 'value', '30'),
                   ('ipmi', 'Temp 24', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 25', 'value', '30'),
                   ('ipmi', 'Temp 25', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 26', 'value', '31'),
                   ('ipmi', 'Temp 26', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 27', 'value', 'disabled'),
                   ('ipmi', 'Temp 28', 'value', '26'),
                   ('ipmi', 'Temp 28', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 29', 'value', '35'),
                   ('ipmi', 'Temp 29', 'unit', 'degrees C'),
                   ('ipmi', 'Temp 30', 'value', '58'),
                   ('ipmi', 'Temp 30', 'unit', 'degrees C'),
                   ('ipmi', 'Memory', 'value', '0x00'),
                   ('ipmi', 'Power Meter', 'value', '170'),
                   ('ipmi', 'Power Meter', 'unit', 'Watts'),
                   ('ipmi', 'Cntlr 1 Bay 1', 'value', '0x01'),
                   ('ipmi', 'Cntlr 1 Bay 2', 'value', '0x01'),
                   ('ipmi', 'Cntlr 1 Bay 3', 'value', '0x00'),
                   ('ipmi', 'Cntlr 1 Bay 4', 'value', '0x01'),
                   ('ipmi', 'Cntlr 2 Bay 5', 'value', '0x00'),
                   ('ipmi', 'Cntlr 2 Bay 6', 'value', '0x00'),
                   ('ipmi', 'Cntlr 2 Bay 7', 'value', '0x01'),
                   ('ipmi', 'Cntlr 2 Bay 8', 'value', '0x01')]

GET_CPUS_RESULT = [('cpu', 'physical', 'number', 2),
                   ('cpu', 'physical_0', 'vendor', 'AuthenticAMD'),
                   ('cpu', 'physical_0', 'product',
                   'AMD: EPYC 7451 24-Core Processor'),
                   ('cpu', 'physical_0', 'cores', 24),
                   ('cpu', 'physical_0', 'threads', 48),
                   ('cpu', 'physical_0', 'family', 23),
                   ('cpu', 'physical_0', 'model', 1),
                   ('cpu', 'physical_0', 'stepping', 2),
                   ('cpu', 'physical_0', 'architecture', 'x86_64'),
                   ('cpu', 'physical_0', 'l1d cache', '32K'),
                   ('cpu', 'physical_0', 'l1i cache', '64K'),
                   ('cpu', 'physical_0', 'l2 cache', '512K'),
                   ('cpu', 'physical_0', 'l3 cache', '8192K'),
                   ('cpu', 'physical_0', 'min_Mhz', 1200.0),
                   ('cpu', 'physical_0', 'max_Mhz', 2300.0),
                   ('cpu', 'physical_0', 'current_Mhz', 1197.549),
                   ('cpu', 'physical_0', 'flags',
                   'fpu vme de pse tsc msr pae mce cx8 apic sep mtrr '
                    'pge mca cmov pat pse36 clflush mmx fxsr sse sse2 '
                    'ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp '
                    'lm constant_tsc rep_good nopl nonstop_tsc '
                    'cpuid extd_apicid amd_dcm aperfmperf pni pclmulqdq '
                    'monitor ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes '
                    'xsave avx f16c rdrand lahf_lm cmp_legacy svm '
                    'extapic cr8_legacy abm sse4a misalignsse '
                    '3dnowprefetch osvw skinit wdt tce topoext '
                    'perfctr_core perfctr_nb bpext perfctr_llc '
                    'mwaitx cpb hw_pstate ssbd ibpb vmmcall '
                    'fsgsbase bmi1 avx2 smep bmi2 rdseed adx smap '
                    'clflushopt sha_ni xsaveopt xsavec xgetbv1 '
                    'xsaves clzero irperf xsaveerptr arat npt lbrv '
                    'svm_lock nrip_save tsc_scale vmcb_clean '
                    'flushbyasid decodeassists pausefilter '
                    'pfthreshold avic v_vmsave_vmload vgif '
                    'overflow_recov succor smca'),
                   ('cpu', 'physical_0', 'threads_per_core', 2),
                   ('cpu', 'physical_1', 'vendor', 'AuthenticAMD'),
                   ('cpu', 'physical_1', 'product',
                   'AMD: EPYC 7451 24-Core Processor'),
                   ('cpu', 'physical_1', 'cores', 24),
                   ('cpu', 'physical_1', 'threads', 48),
                   ('cpu', 'physical_1', 'family', 23),
                   ('cpu', 'physical_1', 'model', 1),
                   ('cpu', 'physical_1', 'stepping', 2),
                   ('cpu', 'physical_1', 'architecture', 'x86_64'),
                   ('cpu', 'physical_1', 'l1d cache', '32K'),
                   ('cpu', 'physical_1', 'l1i cache', '64K'),
                   ('cpu', 'physical_1', 'l2 cache', '512K'),
                   ('cpu', 'physical_1', 'l3 cache', '8192K'),
                   ('cpu', 'physical_1', 'min_Mhz', 1200.0),
                   ('cpu', 'physical_1', 'max_Mhz', 2300.0),
                   ('cpu', 'physical_1', 'current_Mhz', 1197.549),
                   ('cpu', 'physical_1', 'flags',
                   'fpu vme de pse tsc msr pae mce cx8 apic sep mtrr '
                    'pge mca cmov pat pse36 clflush mmx fxsr sse sse2 '
                    'ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp '
                    'lm constant_tsc rep_good nopl nonstop_tsc '
                    'cpuid extd_apicid amd_dcm aperfmperf pni pclmulqdq '
                    'monitor ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes '
                    'xsave avx f16c rdrand lahf_lm cmp_legacy svm '
                    'extapic cr8_legacy abm sse4a misalignsse '
                    '3dnowprefetch osvw skinit wdt tce topoext '
                    'perfctr_core perfctr_nb bpext perfctr_llc '
                    'mwaitx cpb hw_pstate ssbd ibpb vmmcall '
                    'fsgsbase bmi1 avx2 smep bmi2 rdseed adx smap '
                    'clflushopt sha_ni xsaveopt xsavec xgetbv1 '
                    'xsaves clzero irperf xsaveerptr arat npt lbrv '
                    'svm_lock nrip_save tsc_scale vmcb_clean '
                    'flushbyasid decodeassists pausefilter '
                    'pfthreshold avic v_vmsave_vmload vgif '
                    'overflow_recov succor smca'),
                   ('cpu', 'physical_1', 'threads_per_core', 2),
                   ('cpu', 'logical', 'number', 1),
                   ('numa', 'nodes', 'count', 8),
                   ('numa', 'node_0', 'cpu_count', 12),
                   ('numa', 'node_0', 'cpu_mask', '0x3f00000000003f'),
                   ('numa', 'node_1', 'cpu_count', 12),
                   ('numa', 'node_1', 'cpu_mask', '0xfc0000000000fc0'),
                   ('numa', 'node_2', 'cpu_count', 12),
                   ('numa', 'node_2', 'cpu_mask', '0x3f00000000003f000'),
                   ('numa', 'node_3', 'cpu_count', 12),
                   ('numa', 'node_3', 'cpu_mask', '0xfc0000000000fc0000'),
                   ('numa', 'node_4', 'cpu_count', 12),
                   ('numa', 'node_4', 'cpu_mask', '0x3f00000000003f000000'),
                   ('numa', 'node_5', 'cpu_count', 12),
                   ('numa', 'node_5', 'cpu_mask', '0xfc0000000000fc0000000'),
                   ('numa', 'node_6', 'cpu_count', 12),
                   ('numa', 'node_6', 'cpu_mask', '0x3f00000000003f000000000'),
                   ('numa', 'node_7', 'cpu_count', 12),
                   ('numa', 'node_7', 'cpu_mask',
                    '0xfc0000000000fc0000000000')]

GET_CPUS_7302_RESULT = [('cpu', 'physical', 'number', 1),
                        ('cpu', 'physical_0', 'vendor', 'AuthenticAMD'),
                        ('cpu', 'physical_0', 'product',
                         'AMD EPYC 7302P 16-Core Processor'),
                        ('cpu', 'physical_0', 'cores', 16),
                        ('cpu', 'physical_0', 'threads', 32),
                        ('cpu', 'physical_0', 'family', 23),
                        ('cpu', 'physical_0', 'model', 49),
                        ('cpu', 'physical_0', 'stepping', 0),
                        ('cpu', 'physical_0', 'architecture', 'x86_64'),
                        ('cpu', 'physical_0', 'l1d cache', '32K'),
                        ('cpu', 'physical_0', 'l1i cache', '32K'),
                        ('cpu', 'physical_0', 'l2 cache', '512K'),
                        ('cpu', 'physical_0', 'l3 cache', '16384K'),
                        ('cpu', 'physical_0', 'min_Mhz', 1500.0),
                        ('cpu', 'physical_0', 'max_Mhz', 3000.0),
                        ('cpu', 'physical_0', 'current_Mhz', 1794.163),
                        ('cpu', 'physical_0', 'flags',
                         'fpu vme de pse tsc msr pae mce cx8 apic sep mtrr '
                         'pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht '
                         'syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm '
                         'constant_tsc rep_good nopl nonstop_tsc cpuid extd_'
                         'apicid aperfmperf pni pclmulqdq monitor ssse3 fma '
                         'cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx '
                         'f16c rdrand lahf_lm cmp_legacy svm extapic cr8_'
                         'legacy abm sse4a misalignsse 3dnowprefetch osvw ibs '
                         'skinit wdt tce topoext perfctr_core perfctr_nb '
                         'bpext perfctr_llc mwaitx cpb cat_l3 cdp_l3 hw_'
                         'pstate sme ssbd mba sev ibrs ibpb stibp vmmcall '
                         'fsgsbase bmi1 avx2 smep bmi2 cqm rdt_a rdseed adx '
                         'smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 '
                         'xsaves cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_'
                         'local clzero irperf xsaveerptr wbnoinvd arat npt '
                         'lbrv svm_lock nrip_save tsc_scale vmcb_clean '
                         'flushbyasid decodeassists pausefilter pfthreshold '
                         'avic v_vmsave_vmload vgif umip rdpid overflow_recov '
                         'succor smca'),
                        ('cpu', 'physical_0', 'threads_per_core', 2),
                        ('cpu', 'logical', 'number', 32),
                        ('numa', 'nodes', 'count', 8),
                        ('numa', 'node_0', 'cpu_count', 4),
                        ('numa', 'node_0', 'cpu_mask', '0xf0000000f'),
                        ('numa', 'node_1', 'cpu_count', 4),
                        ('numa', 'node_1', 'cpu_mask', '0xf0000000f0'),
                        ('numa', 'node_2', 'cpu_count', 4),
                        ('numa', 'node_2', 'cpu_mask', '0xf0000000f00'),
                        ('numa', 'node_3', 'cpu_count', 4),
                        ('numa', 'node_3', 'cpu_mask', '0xf0000000f000'),
                        ('numa', 'node_4', 'cpu_count', 4),
                        ('numa', 'node_4', 'cpu_mask', '0xf0000000f0000'),
                        ('numa', 'node_5', 'cpu_count', 4),
                        ('numa', 'node_5', 'cpu_mask', '0xf0000000f00000'),
                        ('numa', 'node_6', 'cpu_count', 4),
                        ('numa', 'node_6', 'cpu_mask', '0xf0000000f000000'),
                        ('numa', 'node_7', 'cpu_count', 4),
                        ('numa', 'node_7', 'cpu_mask', '0xf0000000f0000000')]

GET_CPUS_VM_RESULT = [('cpu', 'physical', 'number', 1),
                      ('cpu', 'physical_0', 'vendor', 'GenuineIntel'),
                      ('cpu', 'physical_0', 'product',
                      'Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz'),
                      ('cpu', 'physical_0', 'cores', 2),
                      ('cpu', 'physical_0', 'threads', 2),
                      ('cpu', 'physical_0', 'family', 6),
                      ('cpu', 'physical_0', 'model', 142),
                      ('cpu', 'physical_0', 'stepping', 10),
                      ('cpu', 'physical_0', 'architecture', 'x86_64'),
                      ('cpu', 'physical_0', 'l1d cache', '32K'),
                      ('cpu', 'physical_0', 'l1i cache', '32K'),
                      ('cpu', 'physical_0', 'l2 cache', '256K'),
                      ('cpu', 'physical_0', 'l3 cache', '8192K'),
                      ('cpu', 'physical_0', 'current_Mhz', 2112.002),
                      ('cpu', 'physical_0', 'flags',
                          'fpu vme de pse tsc msr pae mce cx8 apic sep '
                          'mtrr pge mca cmov pat pse36 clflush mmx fxsr '
                          'sse sse2 ht syscall nx rdtscp lm constant_tsc '
                          'rep_good nopl xtopology nonstop_tsc pni '
                          'pclmulqdq ssse3 cx16 pcid sse4_1 sse4_2 x2apic '
                          'movbe popcnt aes xsave avx rdrand hypervisor '
                          'lahf_lm abm 3dnowprefetch fsgsbase avx2 '
                          'invpcid rdseed clflushopt'),
                      ('cpu', 'physical_0', 'threads_per_core', 1),
                      ('cpu', 'logical', 'number', 2),
                      ('numa', 'nodes', 'count', 1),
                      ('numa', 'node_0', 'cpu_count', 2),
                      ('numa', 'node_0', 'cpu_mask', '0x3')]

GET_CPUS_AARCH64_RESULT = [('cpu', 'physical', 'number', 4),
                           ('cpu', 'physical_0', 'vendor', 'APM'),
                           ('cpu', 'physical_0', 'product', 'X-Gene'),
                           ('cpu', 'physical_0', 'cores', 2),
                           ('cpu', 'physical_0', 'threads', 2),
                           ('cpu', 'physical_0', 'model', 0),
                           ('cpu', 'physical_0', 'stepping', 0),
                           ('cpu', 'physical_0', 'architecture', 'aarch64'),
                           ('cpu', 'physical_0', 'l1d cache', 'unknown size'),
                           ('cpu', 'physical_0', 'l1i cache', 'unknown size'),
                           ('cpu', 'physical_0', 'l2 cache', 'unknown size'),
                           ('cpu', 'physical_0', 'flags',
                            'fp asimd evtstrm cpuid'),
                           ('cpu', 'physical_0', 'threads_per_core', 1),
                           ('cpu', 'physical_1', 'vendor', 'APM'),
                           ('cpu', 'physical_1', 'product', 'X-Gene'),
                           ('cpu', 'physical_1', 'cores', 2),
                           ('cpu', 'physical_1', 'threads', 2),
                           ('cpu', 'physical_1', 'model', 0),
                           ('cpu', 'physical_1', 'stepping', 0),
                           ('cpu', 'physical_1', 'architecture', 'aarch64'),
                           ('cpu', 'physical_1', 'l1d cache', 'unknown size'),
                           ('cpu', 'physical_1', 'l1i cache', 'unknown size'),
                           ('cpu', 'physical_1', 'l2 cache', 'unknown size'),
                           ('cpu', 'physical_1', 'flags',
                            'fp asimd evtstrm cpuid'),
                           ('cpu', 'physical_1', 'threads_per_core', 1),
                           ('cpu', 'physical_2', 'vendor', 'APM'),
                           ('cpu', 'physical_2', 'product', 'X-Gene'),
                           ('cpu', 'physical_2', 'cores', 2),
                           ('cpu', 'physical_2', 'threads', 2),
                           ('cpu', 'physical_2', 'model', 0),
                           ('cpu', 'physical_2', 'stepping', 0),
                           ('cpu', 'physical_2', 'architecture', 'aarch64'),
                           ('cpu', 'physical_2', 'l1d cache', 'unknown size'),
                           ('cpu', 'physical_2', 'l1i cache', 'unknown size'),
                           ('cpu', 'physical_2', 'l2 cache', 'unknown size'),
                           ('cpu', 'physical_2', 'flags',
                            'fp asimd evtstrm cpuid'),
                           ('cpu', 'physical_2', 'threads_per_core', 1),
                           ('cpu', 'physical_3', 'vendor', 'APM'),
                           ('cpu', 'physical_3', 'product', 'X-Gene'),
                           ('cpu', 'physical_3', 'cores', 2),
                           ('cpu', 'physical_3', 'threads', 2),
                           ('cpu', 'physical_3', 'model', 0),
                           ('cpu', 'physical_3', 'stepping', 0),
                           ('cpu', 'physical_3', 'architecture', 'aarch64'),
                           ('cpu', 'physical_3', 'l1d cache', 'unknown size'),
                           ('cpu', 'physical_3', 'l1i cache', 'unknown size'),
                           ('cpu', 'physical_3', 'l2 cache', 'unknown size'),
                           ('cpu', 'physical_3', 'flags',
                            'fp asimd evtstrm cpuid'),
                           ('cpu', 'physical_3', 'threads_per_core', 1),
                           ('cpu', 'logical', 'number', 8),
                           ('numa', 'nodes', 'count', 1),
                           ('numa', 'node_0', 'cpu_count', 8),
                           ('numa', 'node_0', 'cpu_mask', 'ff')]

GET_CPUS_PPC64LE = [('cpu', 'physical', 'number', 2),
                    ('cpu', 'physical_0', 'product',
                     'POWER9, altivec supported'),
                    ('cpu', 'physical_0', 'cores', 18),
                    ('cpu', 'physical_0', 'threads', 72),
                    ('cpu', 'physical_0', 'model', '2.2 (pvr 004e 1202)'),
                    ('cpu', 'physical_0', 'architecture', 'ppc64le'),
                    ('cpu', 'physical_0', 'l1d cache', '32K'),
                    ('cpu', 'physical_0', 'l1i cache', '32K'),
                    ('cpu', 'physical_0', 'l2 cache', '512K'),
                    ('cpu', 'physical_0', 'l3 cache', '10240K'),
                    ('cpu', 'physical_0', 'min_Mhz', 2300.0),
                    ('cpu', 'physical_0', 'max_Mhz', 3800.0),
                    ('cpu', 'physical_0', 'threads_per_core', 4),
                    ('cpu', 'physical_1', 'product',
                     'POWER9, altivec supported'),
                    ('cpu', 'physical_1', 'cores', 18),
                    ('cpu', 'physical_1', 'threads', 72),
                    ('cpu', 'physical_1', 'model', '2.2 (pvr 004e 1202)'),
                    ('cpu', 'physical_1', 'architecture', 'ppc64le'),
                    ('cpu', 'physical_1', 'l1d cache', '32K'),
                    ('cpu', 'physical_1', 'l1i cache', '32K'),
                    ('cpu', 'physical_1', 'l2 cache', '512K'),
                    ('cpu', 'physical_1', 'l3 cache', '10240K'),
                    ('cpu', 'physical_1', 'min_Mhz', 2300.0),
                    ('cpu', 'physical_1', 'max_Mhz', 3800.0),
                    ('cpu', 'physical_1', 'threads_per_core', 4),
                    ('cpu', 'logical', 'number', 144),
                    ('numa', 'nodes', 'count', 6),
                    ('numa', 'node_0', 'cpu_count', 72),
                    ('numa', 'node_0', 'cpu_mask', 'ffffffffffffffffff'),
                    ('numa', 'node_8', 'cpu_count', 72),
                    ('numa', 'node_8', 'cpu_mask',
                     'ffffffffffffffffff000000000000000000'),
                    ('numa', 'node_252', 'cpu_count', 0),
                    ('numa', 'node_252', 'cpu_mask', '0'),
                    ('numa', 'node_253', 'cpu_count', 0),
                    ('numa', 'node_253', 'cpu_mask', '0'),
                    ('numa', 'node_254', 'cpu_count', 0),
                    ('numa', 'node_254', 'cpu_mask', '0'),
                    ('numa', 'node_255', 'cpu_count', 0),
                    ('numa', 'node_255', 'cpu_mask', '0')]
