import { Routes } from '@angular/router';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { LandingComponent } from './features/landing/landing.component';
import { PlayerComponent } from './features/player/player.component';
import { LibraryComponent } from './features/library/library.component';
import { PlaylistComponent } from './features/playlist/playlist.component';
import { NotFoundComponent } from './features/404/404.component';
import { SettingsComponent } from './features/user/settings/setting.component';



export const routes: Routes = [
    {
        path: '',
        component: LandingComponent,
    },
    {
        path: 'dashboard',
        component: DashboardComponent,
    },
    {
        path: 'player',
        component: PlayerComponent,
    },
    {
        path: 'library',
        component: LibraryComponent,
    },
    {
        path:'settings',
        component: SettingsComponent,
    },
    {
        path: 'playlist/:id',
        component: PlaylistComponent,
    },
    {
        path: '**',
        component: NotFoundComponent,
        data: { title: '404 - Not Found' }
    } // Esto previene rutas desconocidas

];
