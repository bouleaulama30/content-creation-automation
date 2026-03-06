import React from 'react';
import {AbsoluteFill, OffthreadVideo, Html5Audio, Img, CalculateMetadataFunction} from 'remotion';
import {parseMedia} from '@remotion/media-parser';


type MediaSrcProp = {
  src: string;
};

type MyCompProp = {
  videoSrc: string;
  audioSrc: string;
  logoSrc: string;
}

export const MyComp: React.FC<MyCompProp> = ({videoSrc, audioSrc, logoSrc}) => {
  return (
    <AbsoluteFill>
      <Video src={videoSrc} />
      <Audio src={audioSrc} />
      <Logo src={logoSrc} />
    </AbsoluteFill>
  );
};

export const calculateMetadata: CalculateMetadataFunction<MyCompProp> = async ({props}) => {
  const {slowDurationInSeconds} = await parseMedia({
    src: props.audioSrc,
    fields: {
      slowDurationInSeconds: true,
      // dimensions: true,
    },
  });


  const fps = 30;

  return {
    durationInFrames: Math.floor(slowDurationInSeconds * fps),
    fps,
    // width: dimensions.width,
    // height: dimensions.height,
  };
};

export const Video: React.FC<MediaSrcProp> = ({src}) => {
  return (
      <AbsoluteFill>
        <OffthreadVideo src={src} />
      </AbsoluteFill>
  );
};

export const Logo: React.FC<MediaSrcProp> = ({src}) => {
  return (
    <AbsoluteFill>
        <Img 
           src={src}
            style={{
              transform: 'scale(0.48) translateY(-220px)',
            }}/>
     </AbsoluteFill>
  );
};

export const Audio: React.FC<MediaSrcProp> = ({src}) => {
  return (
    <AbsoluteFill>
      <Html5Audio src={src} />
    </AbsoluteFill>
  );
};