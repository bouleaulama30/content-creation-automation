import "./index.css";
import { Composition, staticFile } from "remotion";
import {Video, BackgroundImage, AudioVideo, calculateMetadata } from "./Composition";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Video"
        component={Video}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
        src: staticFile('video.mp4'),
      }}
        calculateMetadata={calculateMetadata}
      />

      <Composition
        id="BackgroundImage"
        component={BackgroundImage}
        durationInFrames={60}
        fps={30}
        width={1080}
        height={1920}
      />

      <Composition
        id="Audio"
        component={AudioVideo}
        durationInFrames={60}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
