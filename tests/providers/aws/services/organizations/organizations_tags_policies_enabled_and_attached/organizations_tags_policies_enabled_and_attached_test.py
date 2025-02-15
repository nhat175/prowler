from unittest import mock

from prowler.providers.aws.services.organizations.organizations_service import (
    Organization,
    Policy,
)

AWS_REGION = "us-east-1"

# Moto: NotImplementedError: The TAG_POLICY policy type has not been implemented
# Needs to Mock manually


class Test_organizations_tags_policies_enabled_and_attached:
    def test_organization_no_organization(self):
        organizations_client = mock.MagicMock
        organizations_client.region = AWS_REGION
        organizations_client.organizations = [
            Organization(
                arn="",
                id="AWS Organization",
                status="NOT_AVAILABLE",
                master_id="",
            )
        ]

        with mock.patch(
            "prowler.providers.aws.services.organizations.organizations_service.Organizations",
            new=organizations_client,
        ):
            # Test Check
            from prowler.providers.aws.services.organizations.organizations_tags_policies_enabled_and_attached.organizations_tags_policies_enabled_and_attached import (
                organizations_tags_policies_enabled_and_attached,
            )

            check = organizations_tags_policies_enabled_and_attached()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == "AWS Organizations is not in-use for this AWS Account"
            )
            assert result[0].resource_id == "AWS Organization"
            assert result[0].resource_arn == ""
            assert result[0].region == AWS_REGION

    def test_organization_with_tag_policies_not_attached(self):
        organizations_client = mock.MagicMock
        organizations_client.region = AWS_REGION
        organizations_client.organizations = [
            Organization(
                id="o-1234567890",
                arn="arn:aws:organizations::1234567890:organization/o-1234567890",
                status="ACTIVE",
                master_id="1234567890",
                policies=[
                    Policy(
                        id="p-1234567890",
                        arn="arn:aws:organizations::1234567890:policy/o-1234567890/p-1234567890",
                        type="TAG_POLICY",
                        aws_managed=False,
                        content={"tags": {"Owner": {}}},
                        targets=[],
                    )
                ],
                delegated_administrators=None,
            )
        ]

        with mock.patch(
            "prowler.providers.aws.services.organizations.organizations_tags_policies_enabled_and_attached.organizations_tags_policies_enabled_and_attached.organizations_client",
            new=organizations_client,
        ):
            # Test Check
            from prowler.providers.aws.services.organizations.organizations_tags_policies_enabled_and_attached.organizations_tags_policies_enabled_and_attached import (
                organizations_tags_policies_enabled_and_attached,
            )

            check = organizations_tags_policies_enabled_and_attached()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == "AWS Organization o-1234567890 has tag policies enabled but not attached"
            )
            assert result[0].resource_id == "o-1234567890"
            assert (
                result[0].resource_arn
                == "arn:aws:organizations::1234567890:organization/o-1234567890"
            )
            assert result[0].region == AWS_REGION

    def test_organization_with_tag_policies_attached(self):
        organizations_client = mock.MagicMock
        organizations_client.region = AWS_REGION
        organizations_client.organizations = [
            Organization(
                id="o-1234567890",
                arn="arn:aws:organizations::1234567890:organization/o-1234567890",
                status="ACTIVE",
                master_id="1234567890",
                policies=[
                    Policy(
                        id="p-1234567890",
                        arn="arn:aws:organizations::1234567890:policy/o-1234567890/p-1234567890",
                        type="TAG_POLICY",
                        aws_managed=False,
                        content={"tags": {"Owner": {}}},
                        targets=["1234567890"],
                    )
                ],
                delegated_administrators=None,
            )
        ]

        with mock.patch(
            "prowler.providers.aws.services.organizations.organizations_tags_policies_enabled_and_attached.organizations_tags_policies_enabled_and_attached.organizations_client",
            new=organizations_client,
        ):
            # Test Check
            from prowler.providers.aws.services.organizations.organizations_tags_policies_enabled_and_attached.organizations_tags_policies_enabled_and_attached import (
                organizations_tags_policies_enabled_and_attached,
            )

            check = organizations_tags_policies_enabled_and_attached()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == "AWS Organization o-1234567890 has tag policies enabled and attached to an AWS account"
            )
            assert result[0].resource_id == "o-1234567890"
            assert (
                result[0].resource_arn
                == "arn:aws:organizations::1234567890:organization/o-1234567890"
            )
            assert result[0].region == AWS_REGION
