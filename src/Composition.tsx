import React from 'react';
import {AbsoluteFill, OffthreadVideo, Html5Audio, Img, staticFile, CalculateMetadataFunction} from 'remotion';
import {parseMedia} from '@remotion/media-parser';

type MyCompProps = {
  src: string;
};

export const Video: React.FC<MyCompProps> = ({src}) => {
  return (
    <AbsoluteFill>
      <OffthreadVideo src={src} />
      <Html5Audio src={staticFile('audio.mp3')} />
      <AbsoluteFill>
        <Img 
           src={staticFile('logo.png')}
            style={{
              transform: 'scale(0.48) translateY(-220px)',
            }}/>
     </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const calculateMetadata: CalculateMetadataFunction<MyCompProps> = async ({props}) => {
  const {slowDurationInSeconds, dimensions} = await parseMedia({
    src: props.src,
    fields: {
      slowDurationInSeconds: true,
      dimensions: true,
    },
  });

  if (dimensions === null) {
    // For example when passing an MP3 file:
    throw new Error('Not a video file');
  }

  const fps = 30;

  return {
    durationInFrames: Math.floor(slowDurationInSeconds * fps),
    fps,
    width: dimensions.width,
    height: dimensions.height,
  };
};


export const BackgroundImage: React.FC = () => {
  return (
    <AbsoluteFill>
      <Img src={staticFile('logo.png')} />
    </AbsoluteFill>
  );
};

export const AudioVideo = () => {
  return (
    <AbsoluteFill>
      <Html5Audio src={staticFile('audio.mp3')} />
    </AbsoluteFill>
  );
};