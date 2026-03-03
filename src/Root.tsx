import "./index.css";
import { Composition } from "remotion";
import {Video, BackgroundImage, AudioVideo } from "./Composition";

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
