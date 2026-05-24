import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { UserRole } from '../../features/auth/auth-module';
import { AuthService } from '../services/auth.service';

export const roleGuard = (role: UserRole): CanActivateFn => {
  return () => {
    const auth = inject(AuthService);
    const router = inject(Router);

    if (!auth.isAuthenticated()) {
      return router.createUrlTree(['/auth/login']);
    }

    return auth.hasRole(role) ? true : router.createUrlTree(['/']);
  };
};