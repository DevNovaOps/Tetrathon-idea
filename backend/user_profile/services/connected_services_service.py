from user_profile.models import ConnectedBank, ConnectedUPI, ConnectedCard

class ConnectedServicesService:
    @staticmethod
    def get_services(user):
        if not user or not user.is_authenticated:
            return {"banks": [], "upis": [], "cards": []}
        return {
            "banks": ConnectedBank.objects.filter(user=user, is_deleted=False),
            "upis": ConnectedUPI.objects.filter(user=user, is_deleted=False),
            "cards": ConnectedCard.objects.filter(user=user, is_deleted=False),
        }

    @staticmethod
    def add_bank(user, data):
        if not user or not user.is_authenticated:
            return {"error": "Authentication required"}
        bank_name = data.get('bank_name', 'HDFC Bank')
        acc_num = str(data.get('account_number') or data.get('masked_account') or 'XXXXXXXX1234')
        if len(acc_num) > 4:
            masked = "XXXXXXXX" + acc_num[-4:]
        else:
            masked = "XXXXXXXX" + acc_num
        return ConnectedBank.objects.create(
            user=user,
            bank_name=bank_name,
            masked_account=masked,
            ifsc=data.get('ifsc', 'HDFC0000123'),
            account_type=data.get('account_type', 'Savings'),
            verified=True,
            connection_status="Active"
        )

    @staticmethod
    def add_upi(user, data):
        if not user or not user.is_authenticated:
            return {"error": "Authentication required"}
        return ConnectedUPI.objects.create(
            user=user,
            upi_id=data.get('upi_id', f"{user.email.split('@')[0]}@okaxis"),
            upi_app=data.get('upi_app', 'Google Pay'),
            verification_status="Verified"
        )

    @staticmethod
    def add_card(user, data):
        if not user or not user.is_authenticated:
            return {"error": "Authentication required"}
        card_type = data.get('card_type', 'Debit')
        card_num = str(data.get('card_number') or data.get('last_4_digits') or '4589')
        last_4 = card_num[-4:] if len(card_num) >= 4 else card_num.zfill(4)
        masked = "•••• •••• •••• " + last_4
        
        return ConnectedCard.objects.create(
            user=user,
            card_type=card_type,
            issuer=data.get('issuer', 'HDFC Bank'),
            card_holder=data.get('card_holder', user.full_name or "Valued Customer"),
            last_4_digits=last_4,
            masked_number=masked,
            expiry=data.get('expiry', '08/28'),
            status="Active",
            credit_limit=data.get('credit_limit') or (150000.00 if card_type == 'Credit' else None),
            billing_date=data.get('billing_date') or (5 if card_type == 'Credit' else None),
            due_date=data.get('due_date') or (25 if card_type == 'Credit' else None)
        )

    @staticmethod
    def remove_service(user, service_type, id):
        if not user or not user.is_authenticated:
            return False
        model_map = {
            'bank': ConnectedBank,
            'upi': ConnectedUPI,
            'card': ConnectedCard
        }
        model = model_map.get(service_type.lower())
        if not model:
            return False
        try:
            item = model.objects.get(id=id, user=user, is_deleted=False)
            item.is_deleted = True
            item.save()
            return True
        except model.DoesNotExist:
            return False

    @staticmethod
    def seed_default_services(user):
        if not user or not user.is_authenticated:
            return
        if ConnectedBank.objects.filter(user=user, is_deleted=False).exists():
            return

        ConnectedBank.objects.create(
            user=user,
            bank_name="HDFC Bank",
            masked_account="XXXXXXXX3892",
            ifsc="HDFC0000241",
            account_type="Primary Savings",
            verified=True,
            connection_status="Active"
        )
        ConnectedBank.objects.create(
            user=user,
            bank_name="ICICI Bank",
            masked_account="XXXXXXXX8410",
            ifsc="ICIC0001092",
            account_type="Salary Account",
            verified=True,
            connection_status="Active"
        )

        ConnectedUPI.objects.create(
            user=user,
            upi_id=f"{user.email.split('@')[0]}@okhdfcbank",
            upi_app="Google Pay",
            verification_status="Verified"
        )
        ConnectedUPI.objects.create(
            user=user,
            upi_id=f"{user.email.split('@')[0]}@ybl",
            upi_app="PhonePe",
            verification_status="Verified"
        )

        ConnectedCard.objects.create(
            user=user,
            card_type="Debit",
            issuer="HDFC Bank Platinum",
            card_holder=user.full_name or "Dev User",
            last_4_digits="3892",
            masked_number="•••• •••• •••• 3892",
            expiry="09/27",
            status="Active"
        )
        ConnectedCard.objects.create(
            user=user,
            card_type="Credit",
            issuer="ICICI Bank Regalia",
            card_holder=user.full_name or "Dev User",
            last_4_digits="9104",
            masked_number="•••• •••• •••• 9104",
            expiry="11/28",
            status="Active",
            credit_limit=250000.00,
            billing_date=5,
            due_date=25
        )
