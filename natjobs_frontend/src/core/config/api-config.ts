export const API_BASE_URL = "/api";

export function buildWsUrl(path: string, token?: string | null): string {
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const host = window.location.host;
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;

  const url = new URL(`${protocol}://${host}${normalizedPath}`);
  if (token) {
    url.searchParams.set("token", token);
  }

  return url.toString();
}