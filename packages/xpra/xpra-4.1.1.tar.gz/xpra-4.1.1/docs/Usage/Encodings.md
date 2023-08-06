![Encoding](https://xpra.org/icons/encoding.png)

Xpra supports a wide variety of picture and video encodings for sending the window contents to the client fast and efficiently.\
For some background information on picture encodings, see [https://images.guide/](https://images.guide/).

Choosing which encoding to use for a given window is best left to the xpra engine.\
It will make this decision using the window's characteristics (size, state, metadata, etc), network performance (latency, congestion, etc), user preference, client and server capabilities and performance, etc

Generally, if any tuning is needed, instead of trying to guess what should be used and overriding the `encodings` and `encoding` options, it is best to use the `min-speed` and `min-quality` options instead.


***


# Pseudo encodings
The following pseudo encodings just control which actual encodings can be selected by the engine:\
`auto` which is the default, allows all options\
`grayscale` does the same, but without sending colours - which saves some bandwidth (this saving is not always significant)\
`scroll` will try harder to send the screen updates using a list of motion vectors, if possible


# Picture encodings
|Codename|[Bit Depths](../Features/Image-Depth.md)|Characteristics|Details|
|--------|--------------------------|---------------|-------|
|`mmap`|all|fastest|only available with local connections, selected automatically|
|`rgb`|all|very fast|raw RGB pixels, potentially compressed with a stream compressor (ie: `lz4`)|
|`webp`|24 / 32|good|fast, supports transparency, lossy and lossless modes|
|`jpeg`|24|fast|easy to support|
|`png`|24 / 32|slow|easy to support|
|`png/P`|8|slow|only useful for 8-bit [desktop mode](./Start-Desktop.md)|
|`png/L`|8|slow|greyscale|


***


# Video
Using a video stream is often the most efficient way of sending large amounts of screen updates without consuming too much bandwidth.
The xpra engine should automatically detect when it makes sense to switch to a video codec.

|Codename|[Bit Depths](../Features/Image-Depth.md)|Characteristics
|--------|--------------------------|---------------|
|`vp8`|24|fast but less efficient|
|`vp9`|24 / 30|more efficient but somewhat slower|
|`h264`|24 / 30|licensing issues|
|`hevc`|24 / 30|licensing issues - usually slower|

Which ones of these video encodings are available depends on the video encoders enabled:


## Video Encoders
Xpra ships the following encoder modules:
|Codename|Encodings supported|Notes|
|--------|-------------------|-----|
|`vpx`|`vp8`, `vp9`|
|`x264`|`h264`|fast|
|`x265`|`hevc`|slower|
|[`nvenc`](./NVENC.md)|`h264`, `hevc`|fastest (requires hardware)|
|`ffmpeg`|all|capabilities vary|

Which encodings are actually supported by each encoder may vary, depending on the version used, the build options, hardware capabilities, etc.

You can choose which video encoders are loaded at runtime using the `video-encoders` option.

Some of these video encoders may require a colorspace conversion step:


## Colorspace Conversion
These modules are used for:
* converting the pixel data received by the xpra server into a pixel format that can be consumed by the video encoders
* converting the pixel data from the video decoders into a pixel format that can be used to paint the client's window (different windows may have different capabilities)
* up / down scaling the pixel data when needed
|Codename|Colorspaces supported|Notes|
|--------|-------------------|-----|
|`cython`|`r210`, `BGR48`, `GBRP10`, `YUV444P10`|slow but useful for some high bit depth modes|
|`swscale`|`RGB24`, `BGR24`, `0RGB`, `BGR0`, `ARGB`, `BGRA`, `ABGR`, `YUV420P`, `YUV422P`, `YUV444P`, `GBRP`, `NV12`|fast|
|`libyuv`|`BGRX`, `YUV420P`, `NV12`|fastest|

You can choose which colorspace conversion modules are loaded at runtime using the `csc-modules` option.


## Video Decoders
Xpra ships the following decoder modules:
|Codename|Encodings supported|
|--------|-------------------|
|`avcodec2`|all|
|`vpx`|`vp8`, `vp9`|

You can choose which video decoders are loaded at runtime using the `video-decoders` option.


## Diagnostics
List all the encodings available with the current installation:
```shell
xpra encoding
```
(on MS Windows and MacOS, you can also use the `Encodings_info` wrapper)

List all the video codecs and colorspace conversion modules available:
```shell
xpra video
```
Encodings available to the client:
```shell
xpra attach --encoding=help
```
Encodings available to the server:
```shell
xpra start --encoding=help
```


***


# Tuning
Warning: tuning is very often misused and ends up being counterproductive.

## Preventing blurry screen updates
Rather than selecting a lossless picture encoding, which may use far too much bandwidth and cause performance issues:
* make sure that the applications are correctly detected: either using the application's command [content-type](../../fs/share/xpra/content-type) and [content-categories](../../fs/share/xpra/content-categories/10_default.conf) mapping
* raise the `min-quality` and / or lower the `min-speed`
* maybe lower the `auto-refresh` delay - just be aware that the lossless auto-refresh can be costly (as all lossless frames are)

## Quality
Acceptable values range from 1 (lowest) to 100 (lossless). \
Rather than tuning the `quality` option, it is almost always preferable to set the `min-quality` instead. \
Using lower values saves bandwidth and CPU, but the screen updates may become more blurry.

## Speed
Acceptable values range from 1 (lowest) to 100 (lossless). \
Rather than tuning the `speed` option, it is almost always preferable to set the `min-speed` instead. \
Using lower values costs more CPU, which reduces bandwidth consumption but may also lower the framerate.

## Best
The best possible setup is to use [NVENC](./NVENC.md) or another hardware encoder supported by `libva`: hardware encoders compress very well and do so incredibly fast.


## Further reading
* [x264 tradeoffs](http://alax.info/blog/1394)
* [fps vs noise](http://blog.malayter.com/2010/12/presets-versus-quality-in-x264-encoding.html)
* [fps vs size](http://blogs.motokado.com/yoshi/2011/06/25/comparison-of-x264-presets/)
* [Falsehoods programmers believe about video](https://haasn.xyz/posts/2016-12-25-falsehoods-programmers-believe-about-%5Bvideo-stuff%5D.html)

When comparing performance, make sure that you use the right metrics... \
The number of updates per second (aka `fps`) is not always a good one: if there are many small regions, this can be a good or a bad thing.
