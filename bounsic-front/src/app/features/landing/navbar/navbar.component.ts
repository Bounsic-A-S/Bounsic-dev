import { ChangeDetectionStrategy, Component, inject, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ApiService } from '@app/services/song.service';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';

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
  
  ngOnInit() {
    this.miService.getData().pipe(
      catchError(error => {
        console.error('Error obteniendo datos:', error);
        this.datos ="err"
        return of('');
      })
    ).subscribe(response => {
      this.datos = response;
      if (this.datos) console.log(this.datos); 
    });
  }
  
  toggleMobileMenu() {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }
}
