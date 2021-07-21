
## undefined reference to XOpenDisplay/dlopen
### 1. Error
./lib/libwebrtc.a(audio_device_alsa_linux.o)：在函数‘webrtc::AudioDeviceLinuxALSA::Init()’中：
./out/Debug/../../webrtc/modules/audio_device/linux/audio_device_alsa_linux.cc:174：对‘XOpenDisplay’未定义的引用
./lib/libwebrtc.a(audio_device_alsa_linux.o)：在函数‘webrtc::AudioDeviceLinuxALSA::Terminate()’中：
./out/Debug/../../webrtc/modules/audio_device/linux/audio_device_alsa_linux.cc:227：对‘XCloseDisplay’未定义的引用
./lib/libwebrtc.a(audio_device_alsa_linux.o)：在函数‘webrtc::AudioDeviceLinuxALSA::KeyPressed() const’中：
./out/Debug/../../webrtc/modules/audio_device/linux/audio_device_alsa_linux.cc:2208：对‘XQueryKeymap’未定义的引用
./lib/libwebrtc.a(audio_device_pulse_linux.o)：在函数‘webrtc::AudioDeviceLinuxPulse::Init()’中：
./out/Debug/../../webrtc/modules/audio_device/linux/audio_device_pulse_linux.cc:186：对‘XOpenDisplay’未定义的引用
./lib/libwebrtc.a(audio_device_pulse_linux.o)：在函数‘webrtc::AudioDeviceLinuxPulse::Terminate()’中：
./out/Debug/../../webrtc/modules/audio_device/linux/audio_device_pulse_linux.cc:250：对‘XCloseDisplay’未定义的引用
./lib/libwebrtc.a(audio_device_pulse_linux.o)：在函数‘webrtc::AudioDeviceLinuxPulse::KeyPressed() const’中：
./out/Debug/../../webrtc/modules/audio_device/linux/audio_device_pulse_linux.cc:2986：对‘XQueryKeymap’未定义的引用
./lib/libwebrtc.a(latebindingsymboltable_linux.o)：在函数‘webrtc_adm_linux::InternalLoadDll(char const*)’中：
./out/Debug/../../webrtc/modules/audio_device/linux/latebindingsymboltable_linux.cc:37：对‘dlopen’未定义的引用
./lib/libwebrtc.a(latebindingsymboltable_linux.o)：在函数‘webrtc_adm_linux::GetDllError()’中：
./out/Debug/../../webrtc/modules/audio_device/linux/latebindingsymboltable_linux.cc:24：对‘dlerror’未定义的引用
./lib/libwebrtc.a(latebindingsymboltable_linux.o)：在函数‘webrtc_adm_linux::InternalUnloadDll(void*)’中：
./out/Debug/../../webrtc/modules/audio_device/linux/latebindingsymboltable_linux.cc:58：对‘dlclose’未定义的引用
./lib/libwebrtc.a(latebindingsymboltable_linux.o)：在函数‘webrtc_adm_linux::InternalLoadSymbols(void*, int, char const* const*, void**)’中：
./out/Debug/../../webrtc/modules/audio_device/linux/latebindingsymboltable_linux.cc:98：对‘dlerror’未定义的引用
./lib/libwebrtc.a(latebindingsymboltable_linux.o)：在函数‘webrtc_adm_linux::LoadSymbol(void*, char const*, void**)’中：
./out/Debug/../../webrtc/modules/audio_device/linux/latebindingsymboltable_linux.cc:72：对‘dlsym’未定义的引用
./out/Debug/../../webrtc/modules/audio_device/linux/latebindingsymboltable_linux.cc:73：对‘dlerror’未定义的引用
collect2: error: ld returned 1 exit status

### 2. Solution
-lX11 -ldl

## CreateOffer/CreateAnswer never callback OnSuccess/OnFailue
### 1. webrtc CreateOffer/CreateAnswer never callback OnSuccess/OnFailue
solved by this discuss [No callbacks being called in native WebRTC code.](https://groups.google.com/d/msg/discuss-webrtc/VHkHASWivE4/apsjNiyXJQAJ)
>The reason you're not getting any callback on the SetSessionDescriptionObserver is probably that the PeerConnection is created using the current thread as its "signaling thread", which is supposed to run a message loop to process various events. One of those events includes "set session description succeeded (or failed)". So, you should either call "rtc::Thread::Current()->
ProcessMessages(1000)" instead of "Sleep(1000)", or spawn a new rtc::Thead to be used as the signaling thread, and call the alternate CreatePeerConnectionFactory method.


## archive webrtc library
### 1. build the webrtc source by follow the webrtc official site developer guide
[webrtc native-code development](https://webrtc.org/native-code/development/)
### 2. cmd
`cd out/Release`
`ar crs libwebrtc.a $(find . -name '*.o' -not -name '*.main.o')`

##  crash with/without -D_GLIBCXX_DEBUG
### 1. Error
#0  0x00007ffff78ec6c5 in ?? () from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
#1  0x00007ffff78ec71e in ?? () from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
#2  0x000000000041dbd5 in (anonymous namespace)::_Safe_iterator_base::_Safe_iterator_base (this=0x7fffffffcc18,
    __seq=0x7fffffffda38, __constant=true)
    at ../../build/linux/debian_wheezy_amd64-sysroot/usr/lib/gcc/x86_64-linux-gnu/4.6/../../../../include/c++/4.6/debug/safe_base.h:90
#3  0x000000000063f8ac in (anonymous namespace)::_Safe_iterator<__gnu_cxx::__normal_iterator<webrtc::MediaConstraintsInterface::Constraint const*, std::__cxx1998::vector<webrtc::MediaConstraintsInterface::Constraint, std::allocator<webrtc::MediaConstraintsInterface::Constraint> > >, std::__debug::vector<webrtc::MediaConstraintsInterface::Constraint, std::allocator<webrtc::MediaConstraintsInterface::Constraint> > >::_Safe_iterator (this=0x7fffffffcc18, __i=..., __seq=0x7fffffffda20)
    at ../../build/linux/debian_wheezy_amd64-sysroot/usr/lib/gcc/x86_64-linux-gnu/4.6/../../../../include/c++/4.6/debug/safe_iterator.h:123
#4  0x000000000063f0df in (anonymous namespace)::(anonymous namespace)::vector<webrtc::MediaConstraintsInterface::Constraint, std::allocator<webrtc::MediaConstraintsInterface::Constraint> >::begin (this=0x7fffffffda20)
    at ../../build/linux/debian_wheezy_amd64-sysroot/usr/lib/gcc/x86_64-linux-gnu/4.6/../../../../include/c++/4.6/debug/vector:196
#5  0x000000000063e50e in (anonymous namespace)::MediaConstraintsInterface::Constraints::FindFirst (this=0x7fffffffda20,
    key=..., value=0x7fffffffcc80) at ../../webrtc/api/mediaconstraintsinterface.cc:98
#6  0x000000000063e6dc in (anonymous namespace)::FindConstraint (constraints=0x7fffffffda00, key=..., value=0x7fffffffcdaf,
    mandatory_constraints=0x0) at ../../webrtc/api/mediaconstraintsinterface.cc:130
#7  0x000000000063ec01 in (anonymous namespace)::CopyConstraintsIntoRtcConfiguration (constraints=0x7fffffffda00,
    configuration=0x7fffffffcfb8) at ../../webrtc/api/mediaconstraintsinterface.cc:186
#8  0x0000000000641d5b in (anonymous namespace)::PeerConnectionFactory::CreatePeerConnection (this=0x1d835a0,
    configuration_in=..., constraints=0x7fffffffda00, allocator=..., cert_generator=..., observer=0x1d833d0)
    at ../../webrtc/api/peerconnectionfactory.cc:242
#9  0x0000000000647a6c in (anonymous namespace)::PeerConnectionFactoryProxyWithInternal<webrtc::PeerConnectionFactoryInterface>::CreatePeerConnection_ot (this=0x1d7c020, a1=..., a2=0x7fffffffda00, a3=0x0, a4=0x0, a5=0x1d833d0)
    at ../../webrtc/api/peerconnectionfactoryproxy.h:88
#10 0x0000000000647f00 in (anonymous namespace)::MethodFunctor5<webrtc::PeerConnectionFactoryProxyWithInternal<webrtc::PeerConnectionFactoryInterface>, rtc::scoped_refptr<webrtc::PeerConnectionInterface> (webrtc::PeerConnectionFactoryProxyWithInternal<webrtc::PeerConnectionFactoryInterface>::*)(webrtc::PeerConnectionInterface::RTCConfiguration const&, webrtc::MediaConstraintsInterface const*, cricket::PortAllocator*, rtc::RTCCertificateGeneratorInterface*, webrtc::PeerConnectionObserver*), rtc::scoped_refptr<webrtc::PeerConnectionInterface>, webrtc::PeerConnectionInterface::RTCConfiguration const&, webrtc::MediaConstraintsInterface const*, cricket::PortAllocator*, rtc::RTCCertificateGeneratorInterface*, webrtc::PeerConnectionObserver*>::operator() (this=0x7fffffffd688) at ../../webrtc/base/bind.h:630
#11 0x0000000000647db6 in (anonymous namespace)::FunctorMessageHandler<rtc::scoped_refptr<webrtc::PeerConnectionInterface>, rtc::MethodFunctor5<webrtc::PeerConnectionFactoryProxyWithInternal<webrtc::PeerConnectionFactoryInterface>, rtc::scoped_refptr<webrtc::PeerConnectionInterface> (webrtc::PeerConnectionFactoryProxyWithInternal<webrtc::PeerConnectionFactoryInterface>::*)(webrtc::PeerConnectionInterface::RTCConfiguration const&, webrtc::MediaConstraintsInterface const*, cricket::PortAllocator*, rtc::RTCCertificateGeneratorInterface*, webrtc::PeerConnectionObserver*), rtc::scoped_refptr<webrtc::PeerConnectionInterface>, webrtc::PeerConnectionInterface::RTCConfiguration const&, webrtc::MediaConstraintsInterface const*, cricket::PortAllocator*, rtc::RTCCertificateGeneratorInterface*, webrtc::PeerConnectionObserver*> >::OnMessage (this=0x7fffffffd680, msg=0x7fffffffd280)
    at ../../webrtc/base/messagehandler.h:44
#12 0x00000000006ec4a4 in (anonymous namespace)::Thread::Send (this=0x1d7b6f0, posted_from=..., phandler=0x7fffffffd680,
    id=0, pdata=0x0) at ../../webrtc/base/thread.cc:361
#13 0x00000000006eca79 in (anonymous namespace)::Thread::InvokeInternal (this=0x1d7b6f0, posted_from=...,
---Type <return> to continue, or q <return> to quit---
    handler=0x7fffffffd680) at ../../webrtc/base/thread.cc:455
#14 0x000000000064787f in (anonymous namespace)::Thread::Invoke<rtc::scoped_refptr<webrtc::PeerConnectionInterface>, rtc::MethodFunctor5<webrtc::PeerConnectionFactoryProxyWithInternal<webrtc::PeerConnectionFactoryInterface>, rtc::scoped_refptr<webrtc::PeerConnectionInterface> (webrtc::PeerConnectionFactoryProxyWithInternal<webrtc::PeerConnectionFactoryInterface>::*)(webrtc::PeerConnectionInterface::RTCConfiguration const&, webrtc::MediaConstraintsInterface const*, cricket::PortAllocator*, rtc::RTCCertificateGeneratorInterface*, webrtc::PeerConnectionObserver*), rtc::scoped_refptr<webrtc::PeerConnectionInterface>, webrtc::PeerConnectionInterface::RTCConfiguration const&, webrtc::MediaConstraintsInterface const*, cricket::PortAllocator*, rtc::RTCCertificateGeneratorInterface*, webrtc::PeerConnectionObserver*> > (this=0x1d7b6f0, posted_from=..., functor=...)
    at ../../webrtc/base/thread.h:170
#15 0x0000000000645ea7 in (anonymous namespace)::PeerConnectionFactoryProxyWithInternal<webrtc::PeerConnectionFactoryInterface>::CreatePeerConnection (this=0x1d7c020, a1=..., a2=0x7fffffffda00, a3=..., a4=..., a5=0x1d833d0)
    at ../../webrtc/api/peerconnectionfactoryproxy.h:35
#16 0x000000000040bbf8 in KalamodoPeerConnection::CreatePeerConnection (this=0x1d833d0) at main.cc:77
#17 0x000000000040c483 in webrtc_thread (args=0x0) at main.cc:187
#18 0x000000000040c4e1 in main () at main.cc:195

### 2. Solution
keep -D_GLIBCXX_DEBUG micro the same with in webrtc
add or remove
`-D_GLIBCXX_DEBUG=1`
  
## webrtc2sip
Refer [github](https://github.com/DoubangoTelecom/doubango/blob/master/Building_Source_v2_0.md)

`sudo apt install libsrtp-dev libspeex-dev libspeexdsp-dev`
`./autogen.sh && ./configure --with-ssl --with-srtp --with-speexdsp`

ffmpeg version conflict
  

