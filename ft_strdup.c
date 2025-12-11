/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mustafa.el-shdouh@student.42.    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/11 17:04:41 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/11 18:56:25 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
#include "libft.h"
#include <stdlib.h>

char	*ft_strdup(const char *s)
{
	int		len;
	char	*dest;

	len = ft_strlen(s) + 1;
	dest = (char *)malloc(len * sizeof(char));
	if (!dest)
		return (NULL);
	ft_memcpy(dest, s, len);
	return (dest);
}
