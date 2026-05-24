import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';
import { AuthService } from '../../../../core/services/auth.service';

import { PublicProfileComponent } from './public-profile';

describe('PublicProfileComponent', () => {
	let component: PublicProfileComponent;
	let fixture: ComponentFixture<PublicProfileComponent>;

	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [PublicProfileComponent],
			providers: [
				{
					provide: ActivatedRoute,
					useValue: {
						snapshot: {
							params: {
								id: '1',
							},
						},
					},
				},
				{
					provide: AuthService,
					useValue: {
						getPublicProfile: () => of({ id: 1, username: 'test', role: 'seeker' }),
					},
				},
			],
		}).compileComponents();

		fixture = TestBed.createComponent(PublicProfileComponent);
		component = fixture.componentInstance;
		await fixture.whenStable();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
