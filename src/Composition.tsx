import React from 'react';
import {AbsoluteFill, OffthreadVideo, Html5Audio, Img, staticFile} from 'remotion';



export const Video: React.FC = () => {
  return (
    <AbsoluteFill>
      <Img src={staticFile('lion.png')} />
      {/* <OffthreadVideo src={staticFile('video.mp4')}/> */}
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