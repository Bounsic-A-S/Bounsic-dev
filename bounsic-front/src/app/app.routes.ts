import { Routes } from '@angular/router';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { LandingComponent } from './features/landing/landing.component';

export const routes: Routes = [
    {
        path: '',
        component: LandingComponent,
    },
    {
        path: 'dashboard',
        component: DashboardComponent,
    },
];
