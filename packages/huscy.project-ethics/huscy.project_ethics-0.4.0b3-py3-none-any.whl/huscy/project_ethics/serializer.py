from rest_framework import serializers

from huscy.project_ethics import models, services


class EthicBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EthicBoard
        fields = (
            'id',
            'name',
        )


class EthicFileSerializer(serializers.ModelSerializer):
    filetype_name = serializers.SerializerMethodField()

    class Meta:
        model = models.EthicFile
        fields = (
            'ethic',
            'filehandle',
            'filename',
            'filetype',
            'filetype_name',
            'uploaded_at',
            'uploaded_by',
        )
        read_only_fields = 'filename',

    def get_filetype_name(self, ethic_file):
        return ethic_file.get_filetype_display()

    def create(self, validated_data):
        creator = self.context.get('request').user
        return services.create_ethic_file(**validated_data, creator=creator)


class EthicSerializer(serializers.ModelSerializer):
    ethic_board_name = serializers.SerializerMethodField()
    ethic_files = EthicFileSerializer(many=True, read_only=True)

    class Meta:
        model = models.Ethic
        fields = (
            'code',
            'ethic_board',
            'ethic_board_name',
            'ethic_files',
            'id',
            'project',
        )
        read_only_fields = 'project',

    def get_ethic_board_name(self, ethic):
        return ethic.ethic_board and ethic.ethic_board.name

    def create(self, validated_data):
        project = self.context['project']
        return services.create_ethic(project, **validated_data)
