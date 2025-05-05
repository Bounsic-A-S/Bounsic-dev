import { ChangeDetectionStrategy, Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import User from 'src/types/user/User';
import { AuthService } from '@app/services/auth/auth.service';
import { LucideAngularModule, Pencil } from 'lucide-angular';
import { UserService } from '@app/services/auth/user.service';
import { FormsModule } from '@angular/forms';
import UpdateUser from 'src/types/user/UpdateUser';
import { ChangeDetectorRef } from '@angular/core';
import { LoaderComponent } from '@app/shared/ui/loaders/loader.component';


@Component({
  selector: 'user-settings-account',
  standalone: true,
  imports: [CommonModule, TranslateModule, LucideAngularModule, FormsModule,LoaderComponent],
  templateUrl: './account.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingsAccountComponent implements OnInit {
  private authService = inject(AuthService);
  private userService = inject(UserService);
  private cdRef = inject(ChangeDetectorRef);

  public loading = false
  user: User | null = null;
  Pencil = Pencil;
  previewImg: string | null = null;
  selectedImageFile: File | null = null;

  dataToUpdate: UpdateUser = {
    username: '',
    phone: 0,
    country: '',
    profile_img: new File([], "")
  };

  ngOnInit(): void {
    this.user = this.authService.getUserProfile();
    if (this.user) {
      this.dataToUpdate = {
        username: this.user.username,
        phone: this.user.phone,
        country: this.user.country,
        profile_img: new File([], ""),
      };
    }
  }

  onImageChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files?.[0]) {
      const file = input.files[0];
      this.selectedImageFile = file;
      this.previewImg = URL.createObjectURL(file);
    }
  }
  hasChanges(): boolean {
    return (
      this.dataToUpdate.username !== this.user?.username ||
      this.dataToUpdate.phone !== this.user?.phone ||
      this.dataToUpdate.country !== this.user?.country ||
      this.previewImg !== null
    );
  }

  updateUser(): void {
    this.loading = true
    if (!this.user) return;

    const formData = new FormData();
    formData.append('username', this.dataToUpdate.username);
    formData.append('phone', this.dataToUpdate?.phone?.toString());
    formData.append('country', this.dataToUpdate.country);
    if (this.selectedImageFile) {
      formData.append('profile_img', this.selectedImageFile);
    }
    this.userService.updateUser(formData, this.user.id_user).subscribe({
      next: () => {
        const updatedUser: User = {
          ...this.user!,
          username: this.dataToUpdate.username,
          phone: this.dataToUpdate.phone,
          country: this.dataToUpdate.country,
          profile_img: this.previewImg ?? this.user?.profile_img ?? ''
        };
      
        this.authService.setUserProfile(updatedUser);
        this.user = updatedUser;
        this.previewImg = null;
        this.selectedImageFile = null;
        this.cdRef.markForCheck();
        this.loading = false
      },
      error: err => {console.error('Error actualizando usuario:', err)
        console.log('Detalles del error:', err.error);  
        this.loading = false
      }
    });
  }
}
