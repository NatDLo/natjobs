import { inject } from "@angular/core";
import { CanActivateFn, Router } from "@angular/router";
import { catchError, map, of } from "rxjs";
import { AuthService } from "../services/auth.service";

export const guestGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (!auth.token()) {
    return true;
  }

  if (auth.user()) {
    return router.createUrlTree(["/"]);
  }

  return auth.fetchMe().pipe(
    map(() => router.createUrlTree(["/"])),
    catchError(() => {
      auth.logout();
      return of(true);
    })
  );
};