import {AbsoluteFill, Html5Audio, Img, staticFile} from 'remotion';

export const Video: React.FC = () => {
  return (
    <AbsoluteFill>
      <Img src={staticFile('lion.png')} />
      <Html5Audio src={staticFile('audio.mp3')} />
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