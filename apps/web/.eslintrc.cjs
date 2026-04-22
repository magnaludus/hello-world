/** @type {import("eslint").Linter.Config} */
module.exports = {
  root: false,
  extends: ["next/core-web-vitals"],
  parserOptions: {
    project: "./tsconfig.json",
    tsconfigRootDir: __dirname,
  },
};
