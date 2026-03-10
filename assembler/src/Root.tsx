import "./index.css";
import { Composition } from "remotion";
import {MyComp, calculateMetadata } from "./Composition";


const fps = 30;

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
            // durationInFrames: null,
            durationInFrames: Math.floor(1 * fps),
            src: 'video1.mp4',
          },
          {
            durationInFrames: null,
            src: 'video2.mp4',
          },          
          
          {
            durationInFrames: null,
            src: 'video0.mp4',
          },
          {          
            durationInFrames: null,
            src: 'video3.mp4',
          },
          {
            durationInFrames: null,
            src: 'video4.mp4',
          },
        ],
        audioSrc: 'audio.mp3',
        logoSrc: 'logo.png',
      }}
        calculateMetadata={calculateMetadata}
      />
    </>
  );
};
