import { ChangeDetectionStrategy, Component, inject, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ApiService } from '@app/services/song.service';
import { catchError } from 'rxjs/operators';
import { of, firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  standalone: true,
  imports: [RouterModule, CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LandingNavBarComponent implements OnInit {
  isMobileMenuOpen = false;
  private miService = inject(ApiService);
  datos: string = '';

  async ngOnInit() {
    try {
      const response = await firstValueFrom(
        this.miService.getTest().pipe(
          catchError(error => {
            console.error('Error obteniendo datos:', error);
            return of('');
          })
        )
      );

      if (response) {
        this.datos = response;
        if (this.datos) console.log(this.datos);
      }
    } catch (error) {
      console.error("Error en ngOnInit:", error);
    }
  }
  toggleMobileMenu() {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }
}
