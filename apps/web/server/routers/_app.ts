import { router } from "../trpc";
import { componentRouter } from "./component";
import { rifleRouter } from "./rifle";

export const appRouter = router({
  rifle: rifleRouter,
  component: componentRouter,
});

export type AppRouter = typeof appRouter;
