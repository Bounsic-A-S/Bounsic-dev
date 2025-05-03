import { ChangeDetectionStrategy, Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import User from 'src/types/user/User';
import { AuthService } from '@app/services/auth/auth.service';
import { LucideAngularModule, Pencil } from 'lucide-angular';
@Component({
  selector: 'user-settings-account',
  standalone: true,
  imports: [
    CommonModule,
    TranslateModule,
    LucideAngularModule
  ],
  templateUrl: './account.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingsAccountComponent implements OnInit {
  private authService = inject(AuthService);
  user: User | null = null;
  Pencil = Pencil

  ngOnInit(): void {
    this.user = this.authService.getUserProfile()
  }
  previewImg: string | null = null;

onImageChange(event: Event): void {
  const input = event.target as HTMLInputElement;
  if (input.files?.[0]) {
    const file = input.files[0];
    this.previewImg = URL.createObjectURL(file);
    console.log(this.previewImg)
  }
}
}
