import { enableProdMode, importProvidersFrom } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { environment } from './environments/environment';
import { AppComponent } from './app/app.component'; //ROUTES
import { NgxEchartsModule } from 'ngx-echarts';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material/card';
import { provideAnimations } from '@angular/platform-browser/animations';
import { withInterceptorsFromDi, provideHttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { BrowserModule, bootstrapApplication } from '@angular/platform-browser';
import { ClientSideRowModelModule } from '@ag-grid-community/client-side-row-model';
import { ModuleRegistry } from '@ag-grid-community/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RouterModule } from '@angular/router';
import { StoreModule } from '@ngrx/store';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { appConfig } from './app/app.config';
import 'zone.js';
import './polyfills';

if (environment.production) {
  enableProdMode();
}

ModuleRegistry.registerModules([ClientSideRowModelModule]);

// export const ROUTES: Route[] = [
//   {path: 'admin', loadComponent: () => import('./admin/panel.component').then(mod => mod.AdminPanelComponent)},
// ];

// bootstrapApplication(AppComponent, appConfig)
//   .catch((err) => console.error(err));
bootstrapApplication(AppComponent, {
    providers: [
        // {
        //   provide: ENVIRONMENT_INITIALIZER,
        // },
        importProvidersFrom([
            BrowserAnimationsModule,
            StoreModule.forRoot({}),
            StoreDevtoolsModule.instrument(),
            // RouterModule.forRoot(ROUTES),
          ],
          BrowserModule, FormsModule, MatCardModule, 
          MatToolbarModule, MatButtonModule, MatIconModule,
          MatFormFieldModule, MatSelectModule, MatInputModule, 
          FlexLayoutModule, NgxEchartsModule.forRoot({
            /**
             * This will import all modules from echarts.
             * If you only need custom modules,
             * please refer to [Custom Build] section.
             */
            echarts: () => import('echarts'), // or import('./path-to-my-custom-echarts')
        })),
        provideHttpClient(withInterceptorsFromDi()),
        provideAnimations(),
        // {provide: BACKEND_URL, useValue: 'https://photoapp.looknongmodules.com/api'},
        // provideRouter([/* app routes */]),
    ]
})
.then((ref) => {
  // @ts-ignore
  if (window['ngRef']) {
    // @ts-ignore
    window['ngRef'].destroy();
  }
  // @ts-ignore
  window['ngRef'] = ref;
})
.catch((err) => console.error(err));