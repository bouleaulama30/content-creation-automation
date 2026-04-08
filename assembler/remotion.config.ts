/**
 * Note: When using the Node.JS APIs, the config file
 * doesn't apply. Instead, pass options directly to the APIs.
 *
 * All configuration options: https://remotion.dev/docs/config
 */

import { Config } from "@remotion/cli/config";
import { enableTailwind } from '@remotion/tailwind-v4';
import dotenv from 'dotenv';
import dotenvExpand from 'dotenv-expand';
import path from 'path';

const envPath = path.resolve(__dirname, '../.env');
dotenvExpand.expand(dotenv.config({path: envPath}));

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
Config.overrideWebpackConfig(enableTailwind);
