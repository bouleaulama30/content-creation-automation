import "./index.css";
import { Composition, staticFile } from "remotion";
import {MyComp, calculateMetadata } from "./Composition";

// const fps = 30;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MyComp"
        component={MyComp}
        width={1080}
        height={1920}
        defaultProps={{
        videosSrc: [
          {
            durationInFrames: null,
            src: staticFile('video1.mp4'),
          },
          {
            durationInFrames: null,
            src: staticFile('video2.mp4'),
          },          
          {
            durationInFrames: null,
            src: staticFile('video3.mp4'),
          },          
          {
            durationInFrames: null,
            src: staticFile('video4.mp4'),
          },
        ],
        audioSrc: staticFile('audio.mp3'),
        logoSrc: staticFile('logo.png'),
      }}
        calculateMetadata={calculateMetadata}
      />

      {/* <Composition
        id="Logo"
        component={Logo}
        durationInFrames={60}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          src: staticFile('logo.png'),
      }}
      /> */}
    </>
  );
};
